from abc import abstractmethod, ABC
from loguru._logger import Logger
from typing import Any

from apidevtools.simpleorm.schema import Schema
from apidevtools.simpleorm.records import Records


class BaseStorage(ABC):
    def __init__(self, database: str, host: str, port: str | int, user: str, password: str | None, logger: Logger):
        self.database: str = database
        self.host: str = host
        self.port: str | int = port
        self.user: str = user
        self.password: str | None = password

        self.logger: Logger = logger

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
    async def select(self, query: str, args: tuple[Any, ...] = (), schema_type: type[Schema] = None) -> Records:
        ...

    @abstractmethod
    async def insert(self, schema: Schema, schema_type: type = None) -> Schema | dict[str, Any] | None:
        ...

    @abstractmethod
    async def update(self, schema: Schema, where: str, schema_type: type = None) -> Schema | dict[str, Any] | None:
        ...
