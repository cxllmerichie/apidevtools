from pydantic import BaseModel
from abc import abstractmethod as _abstractmethod, ABC
from typing import Any


class Relation:
    def __init__(self, ext_schema_t: type['Schema'], propname: str, rel_schema_t: type['Schema'], where: dict[str, Any]):
        self.where: dict[str, Any] = where
        self.ext_schema_t: type['Schema'] = ext_schema_t
        self.fieldname: str = propname
        self.rel_schema_t: type['Schema'] = rel_schema_t


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
