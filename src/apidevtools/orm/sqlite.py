from typing import Any, MutableMapping, Optional, AsyncGenerator
from functools import cache
import aiosqlite

from .types import CRUD, Connector
from .. import logman


class SQLite(Connector, CRUD):
    __memory = ':memory:'
    _placeholder = '?'
    _constraint_wrapper = "\""
    _value_wrapper = '\''

    def __init__(self, database: str = ':memory:',
                 logger: logman.Logger = logman.logger):
        self.database: str = database if database.endswith(('.sqlite', '.db')) or database == self.__memory else f'{database}.sqlite'

        self.logger: logman.Logger = logger
        self.pool: aiosqlite.Connection | None = None

    async def create_pool(self) -> bool:
        try:
            self.pool = await aiosqlite.connect(database=self.database)
            self.pool.row_factory = aiosqlite.Row
            self.logger.info(f'`ORM.connector: {self.__class__.__name__}` pool created')
            return True
        except Exception as error:
            self.logger.error(error)
            return False

    async def close_pool(self) -> bool:
        try:
            await self.pool.close()
            self.logger.info(f'`ORM.connector: {self.__class__.__name__}` pool closed')
            return True
        except Exception as error:
            self.logger.error(error)
            return False

    # @cache
    # async def columns(self, tablename: str) -> list[str]:
    #     cursor: aiosqlite.Cursor = await self.pool.execute(f'SELECT * FROM {tablename}')
    #     return list(map(lambda x: x[0], cursor.description))

    async def execute(self, query: str, args: tuple[Any, ...] = ())\
            -> bool:
        try:
            await self.pool.execute(query, args) if len(args) else await self.pool.executescript(query)
            await self.pool.commit()
            return True
        except Exception as error:
            self.logger.error(error)
            return False

    async def fetchall(self, query: str, args: tuple[Any, ...] = (), type: type[dict] = dict)\
            -> list[MutableMapping]:
        try:
            cursor: aiosqlite.Cursor = await self.pool.execute(query, args)
            await self.pool.commit()
            return [dict(row) for row in await cursor.fetchall()]
        except Exception as error:
            self.logger.error(error)
            return []

    async def fetchone(self, query: str, args: tuple[Any, ...] = (), type: type[dict] = dict)\
            -> Optional[MutableMapping]:
        try:
            cursor: aiosqlite.Cursor = await self.pool.execute(query, args)
            await self.pool.commit()
            return await cursor.fetchone()
        except Exception as error:
            self.logger.error(error)
            return None

    async def rows(self, query: str, args: tuple[Any, ...] = (), type: type[dict] = dict) \
            -> AsyncGenerator[dict[str, Any], None]:
        try:
            cursor: aiosqlite.Cursor = await self.pool.execute(query, args)
            while True:
                if item := await cursor.fetchone():
                    yield dict(item)
                else:
                    break
        except Exception as error:
            self.logger.error(error)
            pass
