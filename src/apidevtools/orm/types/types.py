from abc import abstractmethod as _abstractmethod, ABC
from pydantic import BaseModel
from typing import Any


class Schema(BaseModel, ABC):
    @property
    @_abstractmethod
    def __tablename__(self) -> str:
        ...

    async def into_db(self) -> 'Schema':
        return self

    async def from_db(self) -> 'Schema':
        return self


Record = dict[str, Any] | Schema
RecordType = type[dict[str, Any] | Schema]
