from abc import abstractmethod as _abstractmethod, ABC
from pydantic import BaseModel
from typing import Any, Dict


class Schema(BaseModel, ABC):
    @property
    @_abstractmethod
    def __tablename__(self) -> str:
        ...

    @property
    @_abstractmethod
    def __primary__(self) -> str:
        ...

    async def into_db(self) -> 'Schema':
        return self

    async def from_db(self) -> 'Schema':
        return self


Record = Dict[str, Any] | Schema
RecordType = type[Record]
