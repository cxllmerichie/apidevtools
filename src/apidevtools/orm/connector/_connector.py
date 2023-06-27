from abc import abstractmethod
from typing import Any, MutableMapping

from ..types import Relation


class Connector:
    def __init__(self, placeholder: str = '%s', constraint_wrapper: str = '', value_wrapper: str = '\''):
        try:
            self.placeholder: str = placeholder
        except AttributeError:
            ...
        self.constraint_wrapper: str = constraint_wrapper
        self.value_wrapper: str = value_wrapper

    @abstractmethod
    async def create_pool(self):
        ...

    @abstractmethod
    async def close_pool(self):
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
