import typing

import marshmallow as ma
import sqlalchemy as sa
from marshmallow_dataclass import dataclass as ma_dataclass
from sqlalchemy import Column, Select
from sqlalchemy.orm import Query

from ..fields import optional_field


def get_query_columns(query: Query) -> typing.Dict[str, Column]:
    columns = {}
    for c in query.selectable.columns:
        for c2 in c.base_columns:
            if c2.name in columns:
                raise ValueError(f'{c2.name} is defined multiple times in the query. Please manually provide the column.')
            columns[c2.name] = c2

    return columns

class SortException(Exception):
    pass


@ma_dataclass
class Sortable:
    '''
        Allows filtering.
        In order to validate that the field is sortable we must know which fields you have.
        This is done by creating a Marshmallow Schema and adding 'sortable=True' to the field metadata.
        Then passing the schems via the Meta.dto_schema

        This strategy was adopted because we expect sortable APIs to be sortable on fields that the API returns.
        Therefore, we expect you to have a Schema that defines the returned object.
    '''

    sort: str = optional_field(
        help='''
            Used to sort the results. Format: "{column}:{direction}". Direction is optional.
            To filter by multiple columns, separate by comma. Example: "sort=country,city:desc"
        ''',
    )

    class Meta:
        # Only way to pass data into the Marshmallow Schema so we can use it in the validator
        dto_schema: ma.Schema = None

    @ma.validates_schema
    def sort_validator(self: ma.Schema, data: dict, **kwargs):
        sort_data: str = data.get('sort')
        if not sort_data or sort_data == 'None':
            return

        errors = []
        parts = sort_data.split(',')
        for part in parts:
            field_parts = part.split(':', 1)
            if not field_parts:
                errors.append('Sort must specify a column name')
                continue

            # Validate that the field name is defined and that sorting is enabled
            if not (
                field_parts[0]
                and (
                    self.Meta.dto_schema
                    and field_parts[0] in self.Meta.dto_schema.declared_fields
                    and self.Meta.dto_schema.declared_fields.get(field_parts[0]).metadata.get('sortable') is True
                )
            ):
                errors.append(f"Invalid sort column '{field_parts[0]}'.")
            if len(field_parts) == 2 and field_parts[1].lower() not in ('asc', 'desc'):
                errors.append("Invalid sort direction. Must be 'asc', or 'desc'.")

        if errors:
            raise ma.ValidationError({'sort': errors})

    def apply_sort(
        self,
        query: Query | Select,
        columns: typing.Optional[typing.Dict[str, Column]] = None,
    ) -> Query | Select:
        '''
            Parses `sort` string and adds order by clauses to the query.
            Default direction is ascending.
            Expected format:
            * comma delimited columns
            * columns and direction delimited by colon

            Example:
                `given_name:desc,family_name`
            This is equivelent to SQL:
                `ORDER BY "given_name" DESC, "family_name" ASC`
        '''
        query = query._clone()

        columns = {} if columns is None else columns
        query_columns = query.columns if isinstance(query, Select) else get_query_columns(query)

        sort_columns = filter(None, self.sort.split(','))  # filter out empty strings
        for sort_column in sort_columns:
            parts = sort_column.split(':')
            # Ignore empty parts
            if not parts:
                continue
            # Validate that sorted column exists.
            elif parts[0] not in query_columns and parts[0] not in columns:
                raise SortException("Sort column '{}' is not supported.".format(parts[0]))

            column = columns[parts[0]] if parts[0] in columns else query_columns[parts[0]]

            if len(parts) == 1:
                query = query.order_by(sa.asc(column))
            else:
                direction = parts[1].upper()
                if direction == 'ASC':
                    query = query.order_by(sa.asc(column))
                elif direction == 'DESC':
                    query = query.order_by(sa.desc(column))
                else:
                    raise SortException("Invalid sort direction. '{}'".format(direction))

        return query
