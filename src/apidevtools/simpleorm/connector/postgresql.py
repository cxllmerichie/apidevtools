from asyncpg.pool import create_pool as _create_pool, Pool as _Pool
from asyncpg.connection import Connection as _Connection
from asyncpg import exceptions as _exceptions
from loguru._logger import Logger
from typing import Any, MutableMapping
import loguru

from ..types import Records, Relation
from .base import Connector


class PostgreSQL(Connector):
    def __init__(self, database: str,
                 host: str = 'localhost', port: int | str = 5432,
                 user: str = 'postgres', password: str | None = None,
                 logger: Logger = loguru.logger):
        self.database: str = database
        self.host: str = host
        self.port: str | int = port
        self.user: str = user
        self.password: str | None = password

        self.logger: Logger = logger

        self.__pool: _Pool | None = None
        self.__connection: _Connection | None = None

    async def create_pool(self) -> bool:
        try:
            self.__pool = await _create_pool(
                database=self.database, host=self.host, port=self.port, user=self.user, password=self.password
            )
        except OSError:
            self.logger.error('Pool creation failed')
        return self.__pool is not None

    async def close_pool(self) -> bool:
        try:
            await self.__pool.expire_connections()
            await self.__pool.close()
            return True
        except AttributeError:
            self.logger.error(f'Attempting to close not acquired pool')
        return False

    async def __aenter__(self) -> _Connection:
        try:
            self.__connection = await self.__pool.acquire()
            return self.__connection
        except _exceptions.InterfaceError:
            self.logger.error('Attempting to create connection with already closed pool')
        except AttributeError:
            self.logger.error('Attempting to create connection without acquired pool')

    async def __aexit__(self, exc_type: Any, exc_value: Any, exc_traceback: Any) -> None:
        try:
            await self.__pool.release(self.__connection)
        except _exceptions.InterfaceError:
            self.logger.error('Attempting to release not acquired connection')

    async def execute(self, query: str, args: tuple[Any, ...] = ()) -> str:
        async with self as connection:
            return await connection.execute(query, *args)

    async def columns(self, tablename: str) -> list[str]:
        query, args = 'SELECT "column_name" FROM information_schema.columns WHERE "table_name" = $1;', (tablename,)
        async with self as connection:
            return [record['column_name'] for record in Records(await connection.fetch(query, *args)).all()]

    async def fetchall(self, query: str, args: tuple[Any, ...] = ()) -> list[MutableMapping]:
        async with self as connection:
            return await connection.fetch(query, *args)

    async def constructor__select_relation(
            self, relation: Relation
    ) -> tuple[str, tuple[Any, ...]]:
        columns, values = ', '.join(relation.columns), tuple(relation.where.values())
        conditions = ' AND '.join([f'"{key}" = ${index + 1}' for index, key in enumerate(relation.where.keys())])
        return f'SELECT {columns} FROM "{relation.tablename}" WHERE {conditions};', values

    async def constructor__select_identity(
            self,
            instance: dict, tablename: str
    ) -> tuple[str, tuple[Any, ...]]:
        conditions = ' AND '.join([f'"{key}" = ${index + 1}' for index, key in enumerate(instance.keys())])
        return f'SELECT * FROM "{tablename}" WHERE {conditions};', tuple(instance.values())

    async def constructor__insert(
            self,
            instance: dict, tablename: str
    ) -> tuple[str, tuple[Any, ...]]:
        placeholders = ', '.join([f'${index + 1}' for index in range(len(instance.keys()))])
        columns, values = str(tuple(instance.keys())).replace("'", '"'), instance.values()
        return f'INSERT INTO "{tablename}" {columns} VALUES ({placeholders}) RETURNING *;', tuple(values)

    async def constructor__update(
            self,
            instance: dict, tablename: str, where: dict[str, Any]
    ) -> tuple[str, tuple[Any, ...]]:
        values = ', '.join([f'"{key}" = ${index + 1}' for index, key in enumerate(instance.keys())])
        conditions = ' AND '.join([f'"{key}" = \'{value}\'' for key, value in where.items()])
        return f'UPDATE "{tablename}" SET {values} WHERE {conditions} RETURNING *;', tuple(instance.values())

    async def constructor__delete(
            self,
            instance: dict, tablename: str
    ) -> tuple[str, tuple[Any, ...]]:
        conditions = ' AND '.join([f'"{key}" = ${index + 1}' for index, key in enumerate(instance.keys())])
        return f'DELETE FROM "{tablename}" WHERE {conditions} RETURNING *;', tuple(instance.values())
