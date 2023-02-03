from typing import Any
from asyncpg.pool import create_pool, Pool
from asyncpg.connection import Connection
from asyncpg import exceptions
from loguru._logger import Logger

from .schema import Schema
from .records import Records
from .base import BaseStorage


class PostgresqlStorage(BaseStorage):
    def __init__(self, logger: Logger, database: str,
                 host: str = 'localhost', port: str | int = 5432,
                 user: str = 'postgres', password: str = None):
        super().__init__(logger, database, host, port, user, password)

        self.__pool: Pool | None = None
        self.__connection: Connection | None = None

    async def create_pool(self) -> bool:
        try:
            self.__pool = await create_pool(database=self.database, host=self.host, port=self.port, user=self.user, password=self.password)
        except OSError:
            self.logger.error('Connection failed')
        return self.__pool is not None

    async def close_pool(self) -> bool:
        try:
            await self.__pool.expire_connections()
            await self.__pool.close()
            return True
        except AttributeError:
            self.logger.error(f'Attempting to close not acquired pool')
        return False

    async def __aenter__(self):
        try:
            self.__connection = await self.__pool.acquire()
            return self.__connection
        except AttributeError:
            self.logger.error('Attempting to create connection with not acquired pool')

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        try:
            await self.__pool.release(self.__connection)
        except exceptions.InterfaceError:
            self.logger.error('Attempting to release not acquired connection')

    async def select(self, query: str, args: tuple[Any, ...] = (), schema_t: type = None) -> Records:
        async with self as connection:
            records = await connection.fetch(query, *args)
        return Records(records, schema_t)

    async def execute(self, query: str, args: tuple[Any, ...] = ()) -> Any:
        async with self as connection:
            return await connection.execute(query, *args)

    async def insert(self, schema: Schema, schema_t: type = None) -> Schema | dict[str, Any] | None:
        placeholders = ', '.join([f'${index + 1}' for index in range(len(schema.dict().keys()))])
        columns, values = str(tuple(schema.dict().keys())).replace("'", '"'), schema.dict().values()
        query, args = f'INSERT INTO "{schema.name()}" {columns} VALUES ({placeholders}) RETURNING *;', values
        async with self as connection:
            records = await connection.fetch(query, *args)
        return Records(records, schema_t).first()

    async def update(self, schema: Schema, where: dict[str, Any], schema_t: type = None) -> Schema | dict[str, Any] | None:
        values = ', '.join([f'"{key}" = ${index + 1}' for index, key in enumerate(schema.dict().keys())])
        conditions = ' and '.join([f'"{key}" = \'{value}\'' for key, value in where.items()])
        query, args = f'UPDATE "{schema.name()}" SET {values} WHERE {conditions} RETURNING *;', tuple(schema.dict().values())
        async with self as connection:
            records = await connection.fetch(query, *args)
        return Records(records, schema_t).first()
