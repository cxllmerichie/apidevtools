from abc import abstractmethod as _abstractmethod, ABC as _ABC
from loguru._logger import Logger
from typing import Any

from .schema import Schema
from .records import Records
from .types import SchemaType, Record, Instance


class BaseORM(_ABC):
    def __init__(self, database: str, host: str, port: str | int, user: str, password: str | None, logger: Logger):
        self.database: str = database
        self.host: str = host
        self.port: str | int = port
        self.user: str = user
        self.password: str | None = password

        self.logger: Logger = logger

    @_abstractmethod
    async def create_pool(self) -> bool:
        ...

    @_abstractmethod
    async def close_pool(self) -> bool:
        ...

    @_abstractmethod
    async def execute(self, query: str, args: tuple[Any, ...] = ()) -> Any:
        ...

    @_abstractmethod
    async def select(self, query: str, args: tuple[Any, ...] = (), schema_t: SchemaType = dict, depth: int = 0) -> Records:
        ...

    @_abstractmethod
    async def insert(self, instance: Instance, schema_t: SchemaType = dict, tablename: str = None) -> Record:
        ...

    @_abstractmethod
    async def update(self, instance: Instance, where: str, schema_t: SchemaType = dict, tablename: str = None) -> Record:
        ...

    @_abstractmethod
    async def delete(self, instance: Instance, schema_t: SchemaType = dict, tablename: str = None) -> Record:
        ...
