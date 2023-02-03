from pydantic import BaseModel
from datetime import datetime, date, time
from abc import ABC, abstractmethod


class Schema(BaseModel, ABC):
    def serializable(self) -> dict[str: str]:
        dictionary = dict(self)
        for key, value in dictionary.items():
            if isinstance(value, (datetime, date, time)):
                dictionary[key] = str(value)
        return dictionary

    @abstractmethod
    def name(self) -> str:
        ...

    def prettify(self) -> 'Schema':
        return self
