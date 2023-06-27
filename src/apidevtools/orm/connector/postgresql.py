import asyncpg as _asyncpg
from typing import Any, MutableMapping

from ..types import Relation
from ._connector import Connector
from ... import logman


class PostgreSQL(Connector):
    def __init__(self, database: str,
                 host: str = 'localhost', port: int | str = 5432,
                 user: str = 'postgres', password: str | None = None,
                 logger: logman.Logger = logman.logger):
        self.database: str = database
        self.host: str = host
        self.port: str | int = port
        self.user: str = user
        self.password: str | None = password

        self.logger: logman.Logger = logger
        self.pool: _asyncpg.pool.Pool | None = None

        super().__init__(..., '', '\'')
        self.placeholder_count: int = 0

    @property
    def placeholder(self):
        self.placeholder_count += 1
        return f'${self.placeholder_count}'

    async def create_pool(self):
        self.pool = await _asyncpg.pool.create_pool(
            database=self.database, host=self.host, port=self.port, user=self.user, password=self.password
        )

    async def close_pool(self) -> bool:
        try:
            await self.pool.expire_connections()
            await self.pool.close()
            return True
        except AttributeError:
            self.logger.error(f'Attempting to close not acquired pool')
            return False

    async def execute(self, query: str, args: tuple[Any, ...] = ()) -> Any:
        try:
            async with self.pool.acquire() as connection:
                return await connection.execute(query, *args)
        except Exception as error:
            self.logger.error(error)

    async def columns(self, tablename: str) -> list[str]:
        query, args = 'SELECT "column_name" FROM "information_schema"."columns" WHERE "table_name" = $1;', (tablename,)
        async with self.pool.acquire() as connection:
            return [dict(record)['column_name'] for record in await connection.fetch(query, *args)]

    async def fetchall(self, query: str, args: tuple[Any, ...] = ()) -> list[MutableMapping]:
        try:
            async with self.pool.acquire() as connection:
                return await connection.fetch(query, *args)
        except Exception as error:
            self.logger.error(error)
            return []
