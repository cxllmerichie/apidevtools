from typing import Any, Optional, AsyncGenerator, Callable, Awaitable
from functools import cache
import asyncpg

from .types import Connector, RecordType, Record, Insert, Select, Update, Delete, Schema, Query, Operation
from .. import logman


class PostgreSQL(Connector, Insert, Select, Update, Delete):
    _placeholder_count: int = 0

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
            self.logger.info(f'{self.__class__.__name__} pool created')
            return True
        except Exception as error:
            self.logger.error(error)
            return False

    async def close_pool(self) -> bool:
        try:
            await self.pool.expire_connections()
            await self.pool.close()
            self.logger.info(f'{self.__class__.__name__} pool created')
            return True
        except AttributeError:
            self.logger.error(f'Attempting to close not acquired pool')
            return False

    # @cache
    # async def columns(self, tablename: str) -> list[str]:
    #     query, args = 'SELECT "column_name" FROM "information_schema"."columns" WHERE "table_name" = $1;', (tablename,)
    #     async with self.pool.acquire() as connection:
    #         return [dict(record)['column_name'] for record in await connection.fetch(query, *args)]
    #
    # def __aiter__(self) -> 'PostgreSQL':
    #     self._records = self.records(self._query, self._qargs, self._type)
    #     return self
    #
    # async def __anext__(self) -> Record:
    #     try:
    #         return next(self._records)
    #     except StopIteration:
    #         raise StopAsyncIteration

    async def execute(self, query: Query, args: tuple[Any, ...] = ()) -> bool:
        query, args, _, _ = await self._parameters(query, args, None)
        try:
            async with self.pool.acquire() as connection:
                await connection.execute(query, *args)
            return True
        except Exception as error:
            self.logger.error(error)
            return False

    async def fetchone(self, query: Query, args: tuple[Any, ...] = (), type: RecordType = dict) -> Optional[Record]:
        query, args, type, unwrap = await self._parameters(query, args, type)
        try:
            async with self.pool.acquire() as connection:
                if record := await connection.fetchrow(query, *args):
                    return await unwrap(record, type)
        except Exception as error:
            self.logger.error(error)
            return None

    async def records(self, query: Query, args: tuple[Any, ...] = (), type: RecordType = dict) -> AsyncGenerator[Record, None]:
        query, args, type, unwrap = await self._parameters(query, args, type)
        try:
            async with self.pool.acquire() as connection:
                async with connection.transaction() as transaction:
                    async for record in connection.cursor(query, *args):
                        yield await unwrap(record, type)
        except Exception as error:
            self.logger.error(error)

    def _unwrapper(self, type: RecordType) -> Callable[[Any, RecordType], Awaitable[Record]]:
        async def to_dict(record: Any, _: RecordType) -> dict[str, Any]:
            return dict(record)

        async def to_schema(record: Any, type: RecordType) -> Schema:
            return await type(**dict(record)).from_db()

        return to_dict if type is dict else to_schema

    @property
    def _placeholder(self):
        self._placeholder_count += 1
        return f'${self._placeholder_count}'
