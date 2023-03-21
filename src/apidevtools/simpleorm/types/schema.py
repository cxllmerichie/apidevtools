from pydantic import BaseModel
from abc import ABC
from abc import abstractmethod as _abstractmethod
from typing import Any


class Relation:
    def __init__(self, tablename: str, where: dict[str, Any], ext_schema_t: 'SchemaType', fieldname: str,
                 rel_schema_t: 'SchemaType' = dict[str, Any], columns: list[str] = None):
        self.tablename: str = tablename
        self.where: dict[str, Any] = where
        self.ext_schema_t: 'SchemaType' = ext_schema_t
        self.fieldname: str = fieldname
        self.rel_schema_t: 'SchemaType' = rel_schema_t
        self.columns: list[str] = columns if columns else ['*']


class Schema(BaseModel, ABC):
    @property
    @_abstractmethod
    def __tablename__(self) -> str:
        """
        Abstract property, supposed to handles name of the database table
        :return:
        """
        ...

    def relations(self) -> list[Relation]:
        return []

    def into_db(self) -> 'Schema':
        return self

    def from_db(self) -> 'Schema':
        return self


SchemaType = type[dict[str, Any] | Schema]
