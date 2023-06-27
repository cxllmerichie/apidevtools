from typing import Any, MutableMapping, Optional, AsyncGenerator
from functools import cache
import asyncpg

from .types import CRUD, Connector
from .. import logman


class PostgreSQL(Connector, CRUD):
    _placeholder_count: int = 0
    _constraint_wrapper = ''
    _value_wrapper = '\''

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
        self.pool: asyncpg.pool.Pool | None = None

    async def create_pool(self):
        try:
            self.pool = await asyncpg.pool.create_pool(
                database=self.database, host=self.host, port=self.port, user=self.user, password=self.password
            )
            self.logger.info(f'`ORM.connector: {self.__class__.__name__}` pool created')
            return True
        except Exception as error:
            self.logger.error(error)
            return False

    async def close_pool(self) -> bool:
        try:
            await self.pool.expire_connections()
            await self.pool.close()
            self.logger.info(f'`ORM.connector: {self.__class__.__name__}` pool created')
            return True
        except AttributeError:
            self.logger.error(f'Attempting to close not acquired pool')
            return False

    # @cache
    # async def columns(self, tablename: str) -> list[str]:
    #     query, args = 'SELECT "column_name" FROM "information_schema"."columns" WHERE "table_name" = $1;', (tablename,)
    #     async with self.pool.acquire() as connection:
    #         return [dict(record)['column_name'] for record in await connection.fetch(query, *args)]

    async def execute(self, query: str, args: tuple[Any, ...] = ()) -> Any:
        try:
            async with self.pool.acquire() as connection:
                return await connection.execute(query, *args)
        except Exception as error:
            self.logger.error(error)

    async def fetchall(self, query: str, args: tuple[Any, ...] = (), type: type[dict] = dict)\
            -> list[MutableMapping]:
        try:
            return [row async for row in self.rows(query, args, type)]
            # async with self.pool.acquire() as connection:
            #     row = await connection.fetch(query, *args)
            #     return type(**dict(row))
        except Exception as error:
            self.logger.error(error)
            return []

    async def fetchone(self, query: str, args: tuple[Any, ...] = (), type: type[dict] = dict)\
            -> Optional[MutableMapping]:
        try:
            async with self.pool.acquire() as connection:
                row = await connection.fetchrow(query, *args)
                return type(**dict(row))
        except Exception as error:
            self.logger.error(error)
            return None

    async def rows(self, query: str, args: tuple[Any, ...] = (), type: type[dict] = dict)\
            -> AsyncGenerator[dict[str, Any], None]:
        try:
            async with self.pool.acquire() as connection:
                async with connection.transaction() as transaction:
                    async for row in connection.cursor(query, *args):
                        yield type(**dict(row))
        except Exception as error:
            self.logger.error(error)
            pass

    @property
    def _placeholder(self):
        self._placeholder_count += 1
        return f'${self._placeholder_count}'
