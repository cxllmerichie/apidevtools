from abc import abstractmethod, ABC
from loguru._logger import Logger
from typing import Any

from .schema import Schema
from .records import Records


class BaseStorage(ABC):
    def __init__(self, logger: Logger, database: str, host: str, port: str | int, user: str, password: str | None):
        self.logger: Logger = logger

        self.database: str = database
        self.host: str = host
        self.port: int = port
        self.user: str = user
        self.password: str = password

    @abstractmethod
    async def create_pool(self) -> bool:
        ...

    @abstractmethod
    async def close_pool(self) -> bool:
        ...

    @abstractmethod
    async def select(self, query: str, args: tuple[Any, ...] = (), schema_type: type[Schema] = None) -> Records:
        ...

    @abstractmethod
    async def execute(self, query: str, args: tuple[Any, ...] = ()) -> Any:
        ...

    @abstractmethod
    async def insert(self, schema: Schema, schema_type: type = None) -> Schema | dict[str, Any] | None:
        ...

    @abstractmethod
    async def update(self, schema: Schema, where: str, schema_type: type = None) -> Schema | dict[str, Any] | None:
        ...
