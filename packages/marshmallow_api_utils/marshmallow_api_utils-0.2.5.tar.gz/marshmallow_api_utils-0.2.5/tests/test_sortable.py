import datetime as dt

import pytest
import sqlalchemy.types as st
from marshmallow import ValidationError
from marshmallow_dataclass import dataclass as ma_dataclass
from sqlalchemy import Column, Select, select
from sqlalchemy.orm import DeclarativeBase, Query, Session

from marshmallow_api_utils.fields import optional_field
from marshmallow_api_utils.ma_dataclass import MaDataclass
from marshmallow_api_utils.models.sortable import Sortable

from .utils import assert_string_minified


class Base(DeclarativeBase):
    pass


class DBModel(Base):
    __tablename__ = 'db_model'

    id = Column(st.Integer, primary_key=True)
    name = Column(st.String)
    birthdate = Column(st.Date)
    age = Column(st.Integer)


@ma_dataclass
class DTO(MaDataclass):
    name: str = optional_field()
    birthdate: dt.date = optional_field()
    age: int = optional_field(sortable=False)


@ma_dataclass
class QueryParams(Sortable, MaDataclass):
    class Meta:
        dto_schema = DTO.Schema()


@ma_dataclass
class NoMetaQueryParams(Sortable, MaDataclass):
    pass


def test_sort_validator():
    qp = QueryParams.loads('{"sort": "name:asc"}')

    assert qp == QueryParams(
        sort="name:asc",
    )


def test_sort_no_direction():
    qp = QueryParams.loads('{"sort": "name"}')

    assert qp == QueryParams(
        sort="name",
    )


def test_sort_multiple():
    qp = QueryParams.loads('{"sort": "name:asc,birthdate:DESC"}')

    assert qp == QueryParams(
        sort="name:asc,birthdate:DESC",
    )


def test_sort_non_sortable_field():
    with pytest.raises(ValidationError) as ex:
        QueryParams.loads('{"sort": "age:asc"}')
        assert ex.value.data == {
            'sort': ["Invalid sort column 'age'"],
        }


def test_sort_undefined_field():
    with pytest.raises(ValidationError) as ex:
        QueryParams.loads('{"sort": "foobar:asc"}')
        assert ex.value.data == {
            'sort': ["Invalid sort column 'foobar'"],
        }


def test_sort_invalid_direction():
    with pytest.raises(ValidationError) as ex:
        QueryParams.loads('{"sort": "name:foobar"}')
        assert ex.value.data == {
            'sort': ["Invalid sort direction. Must be 'asc', or 'desc'."],
        }


def test_sort_no_meta():
    with pytest.raises(ValidationError) as ex:
        NoMetaQueryParams.loads('{"sort": "age:asc"}')
        assert ex.value.data == {
            'sort': ["Invalid sort column 'age'"],
        }


def test_sort_multiple_sql_expr_select():
    qp = QueryParams.loads('{"sort": "name:asc,birthdate:DESC"}')

    stmt: Select = select(DBModel)
    sorted_stmt = qp.apply_sort(stmt)

    assert_string_minified(
        str(sorted_stmt),
        '''
            SELECT db_model.id, db_model.name, db_model.birthdate, db_model.age
            FROM db_model
            ORDER BY anon_1.name ASC, anon_1.birthdate DESC
        ''',
    )


def test_sort_multiple_sql_expr_query():
    qp = QueryParams.loads('{"sort": "name:asc,birthdate:DESC"}')

    query: Query = Session().query(DBModel)
    sorted_query = qp.apply_sort(query)

    assert_string_minified(
        str(sorted_query),
        '''
            SELECT
                db_model.id AS db_model_id,
                db_model.name AS db_model_name,
                db_model.birthdate AS db_model_birthdate,
                db_model.age AS db_model_age
            FROM db_model
            ORDER BY db_model.name ASC, db_model.birthdate DESC
        ''',
    )
