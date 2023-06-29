from typing import Any, Optional, AsyncGenerator, Callable, Awaitable
from functools import cache
import aiosqlite

from .types import Connector, RecordType, Record, Insert, Select, Update, Delete, Query, Schema
from .. import logman


class SQLite(Connector, Insert, Select, Update, Delete):
    _placeholder = '?'

    __memory = ':memory:'

    def __init__(self, database: str = ':memory:',
                 logger: logman.Logger = logman.logger):
        self.database: str = database if database.endswith(('.sqlite', '.db')) or database == self.__memory else f'{database}.sqlite'

        self.logger: logman.Logger = logger
        self.pool: aiosqlite.Connection | None = None

    async def create_pool(self) -> bool:
        try:
            self.pool = await aiosqlite.connect(database=self.database)
            self.pool.row_factory = aiosqlite.Row
            self.logger.info(f'{self.__class__.__name__} pool created')
            return True
        except Exception as error:
            self.logger.error(error)
            return False

    async def close_pool(self) -> bool:
        try:
            await self.pool.close()
            self.logger.info(f'{self.__class__.__name__} pool closed')
            return True
        except Exception as error:
            self.logger.error(error)
            return False

    # @cache
    # async def columns(self, tablename: str) -> list[str]:
    #     cursor: aiosqlite.Cursor = await self.pool.execute(f'SELECT * FROM {tablename}')
    #     return list(map(lambda x: x[0], cursor.description))

    async def execute(self, query: Query, args: tuple[Any, ...] = ()) -> bool:
        query, args, _, _ = await self._parameters(query, args, None)
        try:
            await self.pool.execute(query, args) if len(args) else await self.pool.executescript(query)
            await self.pool.commit()
            return True
        except Exception as error:
            self.logger.error(error)
            return False

    async def fetchone(self, query: Query, args: tuple[Any, ...] = (), type: RecordType = dict) -> Optional[Record]:
        query, args, type, unwrap = await self._parameters(query, args, type)
        try:
            cursor: aiosqlite.Cursor = await self.pool.execute(query, args)
            record = await cursor.fetchone()
            await self.pool.commit()
            return await unwrap(record, type)
        except Exception as error:
            self.logger.error(error)
            return None

    async def records(self, query: Query, args: tuple[Any, ...] = (), type: RecordType = dict) -> AsyncGenerator[Record, None]:
        query, args, type, unwrap = await self._parameters(query, args, type)
        try:
            cursor: aiosqlite.Cursor = await self.pool.execute(query, args)
            await self.pool.commit()
            while record := await cursor.fetchone():
                yield await unwrap(record, type)
        except Exception as error:
            self.logger.error(error)

    def _unwrapper(self, type: RecordType) -> Callable[[Any, RecordType], Awaitable[Record]]:
        async def to_dict(record: Any, _: RecordType) -> dict[str, Any]:
            return dict(record) if record else None

        async def to_schema(record: Any, type: RecordType) -> Schema:
            return await type(**dict(record)).from_db() if record else None

        return to_dict if type is dict else to_schema
