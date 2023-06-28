from typing import Any, Optional, AsyncGenerator, Callable, Awaitable
from abc import abstractmethod

from .types import RecordType, Record
from ._operations import Operation
from ._operations import Query


class Connector:
    _placeholder: str = '%s'
    _constraint_wrapper: str = ''
    _value_wrapper: str = '\''

    @abstractmethod
    async def create_pool(self):
        ...

    @abstractmethod
    async def close_pool(self):
        ...

    # @abstractmethod
    # async def columns(self, tablename: str) -> list[str]:
    #     ...

    @abstractmethod
    def __aiter__(self):
        return self.records(f'{self._query[:-1]};', self._qargs, self._type)  # noqa

    @abstractmethod
    def __anext__(self) -> Record:
        try:
            return anext(self)
        except StopIteration:
            raise StopAsyncIteration

    @abstractmethod
    def _unwrapper(self, type: RecordType) -> Callable[[Any, RecordType], Awaitable[Record]]:
        ...

    async def _parameters(self, query: Query, args: tuple[Any, ...], type: RecordType):
        if isinstance(query, Operation):
            query, args, type = f'{self._query[:-1]};', self._qargs, self._type  # noqa
        return query, args, type, self._unwrapper(type)

    @abstractmethod
    async def execute(self, query: Query, args: tuple[Any, ...] = ()) -> bool:
        ...

    async def fetchall(self, query: Query, args: tuple[Any, ...] = (), type: RecordType = dict) -> list[Record]:
        try:
            return [record async for record in self.records(query, args, type)]  # noqa
        except Exception as error:
            self.logger.error(error)  # noqa
            return []

    @abstractmethod
    async def fetchone(self, query: Query, args: tuple[Any, ...] = (), type: RecordType = dict) -> Optional[Record]:
        ...

    @abstractmethod
    async def records(self, query: Query, args: tuple[Any, ...] = (), type: RecordType = dict) -> AsyncGenerator[Record, None]:
        ...
