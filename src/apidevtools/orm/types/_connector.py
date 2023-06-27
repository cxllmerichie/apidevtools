from typing import Any, MutableMapping, Optional, AsyncGenerator
from abc import abstractmethod


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
    async def execute(self, query: str, args: tuple[Any, ...] = ()) -> Any:
        ...

    @abstractmethod
    async def fetchall(self, query: str, args: tuple[Any, ...] = (), type: type[dict] = dict) -> list[MutableMapping]:
        ...

    @abstractmethod
    async def fetchone(self, query: str, args: tuple[Any, ...] = (), type: type[dict] = dict) -> Optional[MutableMapping]:
        ...

    @abstractmethod
    async def rows(self, query: str, args: tuple[Any, ...] = (), type: type[dict] = dict) -> AsyncGenerator[dict[str, Any], None]:
        ...
