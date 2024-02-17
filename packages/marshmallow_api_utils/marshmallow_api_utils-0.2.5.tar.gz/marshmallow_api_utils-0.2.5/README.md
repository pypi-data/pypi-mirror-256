# Marshmallow API Utilities

A collection of tools for REST API development with Marshmallow.

| | |
| --- | --- |
| Package | [![PyPI - Version](https://img.shields.io/pypi/v/marshmallow_api_utils.svg?logo=pypi&label=PyPI&logoColor=gold)](https://pypi.org/project/marshmallow_api_utils/) [![PyPI - Downloads](https://img.shields.io/pypi/dm/marshmallow_api_utils.svg?color=blue&label=Downloads&logo=pypi&logoColor=gold)](https://pypi.org/project/marshmallow_api_utils/) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/marshmallow_api_utils.svg?logo=python&label=Python&logoColor=gold)](https://pypi.org/project/marshmallow_api_utils/) |
| Meta | [![linting - Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v0.json)](https://github.com/charliermarsh/ruff) [![License - MIT](https://img.shields.io/badge/license-MIT-9400d3.svg)](https://spdx.org/licenses/) |

## Basic usage

```python
from datetime import date
from flask import Flask
from flask_smorest import Api
from marshmallow_dataclass import dataclass as ma_dataclass
from sqlalchemy import Column, Select, select
from sqlalchemy.orm import DeclarativeBase

from marshmallow_api_utils.fields import dump_only_field, optional_field, required_field
from marshmallow_api_utils.ma_dataclass import MaDataclass
from marshmallow_api_utils.models.sortable import Sortable


class Base(DeclarativeBase):
    pass


class Pet(Base):
    __tablename__ = 'pets'

    id = Column(st.Integer, primary_key=True)
    name = Column(st.String)
    birthdate = Column(st.Date)


@ma_dataclass
class PetDTO(MaDataclass):
    id: int = dump_only_field()
    name: str = required_field(help='This will show up in the OpenAPI docs.')
    birthdate: dt.date = optional_field()
    age: int = dump_only_field(sortable=False)

    @ma.pre_dump
    def add_age(self, data, many, **kwargs):
      data['age'] = int((date.today() - data.birthdate) / 365.25)
      return data


@ma_dataclass
class PetQueryParams(Sortable, MaDataclass):
    class Meta:
        dto_schema = PetDTO.Schema()


flask = Flask(__name__)
app.config["API_TITLE"] = "My API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.2"
api = Api(app)

blp = Blueprint("pets", "pets", url_prefix="/pets", description="Operations on pets")

@blp.route("/")
class Pets(MethodView):

    @blp.arguments(PetQueryParams.Schema, location="query")
    @blp.response(200, Pet.Schema(many=True))
    def get(self, query_params: PetQueryParams):
        """List pets"""
        stmt = select(Pet)
        stmt = query_params.apply_sort(stmt)

        return stmt.all()
```

## License

Marshmallow API Utilities is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
