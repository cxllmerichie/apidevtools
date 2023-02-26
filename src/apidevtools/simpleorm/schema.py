from pydantic import BaseModel as _BaseModel
from abc import ABC as _ABC, abstractmethod as _abstractmethod
from typing import Any
import datetime

from .relation import Relation


class Schema(_BaseModel, _ABC):
    @property
    @_abstractmethod
    def __tablename__(self) -> str:
        """
        Abstract property, supposed to handle name of the database table to be used together with simpleorm.storage
        :return:
        """
        ...

    @property
    def tablename(self) -> str:
        """
        method, which will be used in the simpleorm.storage methods
        :return:
        """
        return self.__tablename__

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

