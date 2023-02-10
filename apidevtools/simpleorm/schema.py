from pydantic import BaseModel
from datetime import datetime, date, time
from abc import ABC, abstractmethod
from typing import Any


class Schema(BaseModel, ABC):
    def serializable(self, types: tuple[type, ...] = (datetime, date, time)) -> dict[str: Any]:
        """
        Returns python dictionary of values which will not trigger FastAPI error related to not serializable objects
        :param types:
        :return:
        """
        return {key: str(value) if isinstance(value, types) else value for key, value in dict(self).items()}

    @property
    @abstractmethod
    def __tablename__(self) -> str:
        """
        Abstract property, supposed to handle name of the database table to be used together with simpleorm.storage
        :return:
        """
        ...

    @property
    def tablename(self):
        """
        method, which will be used in the simpleorm.storage methods
        :return:
        """
        return self.__tablename__

    def pretty(self) -> 'Schema':
        """
        Assign prettified values to Schema.properties.
        For instance: self.email = self.email.lower(); self.surname = self.surname.capitalize; return self;
        :return:
        """
        return self
