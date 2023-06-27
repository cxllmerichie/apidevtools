from pydantic import BaseModel
from abc import abstractmethod as _abstractmethod, ABC
from typing import MutableMapping, Any, Coroutine, Iterator
from contextlib import suppress as _suppress

from ...utils import is_dict as _is_dict
from ._operations import Insert, Select, Update, Delete


class CRUD(Insert, Select, Update, Delete):
    ...


class Schema(BaseModel, ABC):
    @property
    @_abstractmethod
    def __tablename__(self) -> str:
        ...

    async def into_db(self) -> 'Schema':
        return self

    async def from_db(self) -> 'Schema':
        return self


Instance = dict[str, Any] | Schema
Record = Instance | None
RecordType = type[Instance]


class Records:
    def __init__(self, records: list[MutableMapping], record_t: RecordType = dict[str, Any]):
        self.record_t: RecordType = record_t
        self._unwrap: Coroutine[Any, Any, Instance] = self._unwrapper()
        self._records: list[MutableMapping] = records
        self._aiter: Iterator = iter(records)

    def _unwrapper(self) -> Coroutine[Any, Any, Instance]:
        async def unwrap_to_dict(record: MutableMapping) -> dict[str, Any]:
            return dict(record)

        async def unwrap_to_schema(record: MutableMapping) -> Schema:
            return await self.record_t(**dict(record)).from_db()

        return unwrap_to_dict if _is_dict(self.record_t) else unwrap_to_schema

    def __len__(self) -> int:
        return len(self._records)

    def __aiter__(self) -> 'Records':
        return self

    async def __anext__(self) -> Instance:
        try:
            return await self._unwrap(next(self._aiter))
        except StopIteration:
            raise StopAsyncIteration

    async def all(self) -> list[Instance]:
        return [await self._unwrap(record) for record in self._records]

    async def first(self) -> Record:
        try:
            return await self._unwrap(self._records[0])
        except IndexError:
            return None

    async def last(self) -> Record:
        try:
            return await self._unwrap(self._records[-1])
        except IndexError:
            return None
