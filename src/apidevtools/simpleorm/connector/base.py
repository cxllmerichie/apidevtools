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
    async def __aenter__(self) -> 'Connection':
        ...

    @abstractmethod
    async def __aexit__(self, exc_type: Any, exc_value: Any, exc_traceback: Any) -> None:
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
    async def constructor__select_relation(self, *args, **kwargs) -> tuple[str, tuple[Any, ...]]:
        ...

    @abstractmethod
    async def constructor__select_identity(self, *args, **kwargs) -> tuple[str, tuple[Any, ...]]:
        ...

    @abstractmethod
    async def constructor__insert(self, *args, **kwargs) -> tuple[str, tuple[Any, ...]]:
        ...

    @abstractmethod
    async def constructor__update(self, *args, **kwargs) -> tuple[str, tuple[Any, ...]]:
        ...

    @abstractmethod
    async def constructor__delete(self, *args, **kwargs) -> tuple[str, tuple[Any, ...]]:
        ...
