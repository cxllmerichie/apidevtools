from abc import ABC, abstractmethod
from typing import Any, MutableMapping


class Connector(ABC):
    @abstractmethod
    def __init__(self, database: str, host: str, port: int | str, user: str, password: str | None):
        ...

    @abstractmethod
    async def create_pool(self) -> bool:
        ...

    @abstractmethod
    async def close_pool(self) -> bool:
        ...

    @abstractmethod
    async def execute(self, query: str, args: tuple[Any, ...] = ()) -> Any:
        ...

    @abstractmethod
    async def columns(self, tablename: str) -> list[str]:
        ...

    @abstractmethod
    async def fetchall(self, query: str, args: tuple[Any, ...] = ()) -> list[MutableMapping]:
        ...

    @abstractmethod
    async def _constructor__select_relation(self, *args, **kwargs) -> tuple[str, tuple[Any, ...]]:
        ...

    @abstractmethod
    async def _constructor__select_instance(self, *args, **kwargs) -> tuple[str, tuple[Any, ...]]:
        ...

    @abstractmethod
    async def _constructor__insert_instance(self, *args, **kwargs) -> tuple[str, tuple[Any, ...]]:
        ...

    @abstractmethod
    async def _constructor__update_instance(self, *args, **kwargs) -> tuple[str, tuple[Any, ...]]:
        ...

    @abstractmethod
    async def _constructor__delete_instance(self, *args, **kwargs) -> tuple[str, tuple[Any, ...]]:
        ...
