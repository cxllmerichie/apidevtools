from pydantic import BaseModel
from datetime import datetime, date, time
from abc import ABC, abstractmethod
from typing import Any


class Schema(BaseModel, ABC):
    def serializable(self, types: tuple[type, ...] = (datetime, date, time)) -> dict[str: Any]:
        return {key: str(value) if isinstance(value, types) else value for key, value in dict(self).items()}

    @abstractmethod
    def name(self) -> str:
        ...

    def pretty(self) -> 'Schema':
        return self
