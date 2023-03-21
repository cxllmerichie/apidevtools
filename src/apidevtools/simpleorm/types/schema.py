from pydantic import BaseModel
from abc import ABC
import datetime
from abc import abstractmethod as _abstractmethod
from typing import Any

from .relation import Relation


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

    def serializable(self, types: tuple[type, ...] = (datetime.datetime, datetime.date, datetime.time)) -> dict[str: Any]:
        """
        Returns python dictionary of values which will not trigger FastAPI error related to not serializable objects
        :param types:
        :return:
        """
        return {key: str(value) if isinstance(value, types) else value for key, value in dict(self).items()}

    def into_db(self) -> 'Schema':
        return self

    def from_db(self) -> 'Schema':
        return self


SchemaType = type[dict[str, Any] | Schema]
