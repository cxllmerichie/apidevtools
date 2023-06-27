import aiosqlite as _aiosqlite
from typing import Any, MutableMapping

from ..types import Relation
from ._connector import Connector
from ... import logman


class SQLite(Connector):
    __memory = ':memory:'

    def __init__(self, database: str = ':memory:',
                 logger: logman.Logger = logman.logger):
        self.database: str = database if database.endswith(('.sqlite', '.db')) or database == self.__memory else f'{database}.sqlite'

        self.logger: logman.Logger = logger
        self.pool: _aiosqlite.Connection | None = None

        super().__init__(placeholder='?', constraint_wrapper="\"", value_wrapper='\'')

    async def create_pool(self) -> bool:
        try:
            self.pool = await _aiosqlite.connect(database=self.database)
            return True
        except Exception as error:
            self.logger.error(error)
            return False

    async def close_pool(self) -> bool:
        try:
            await self.pool.close()
            return True
        except Exception as error:
            self.logger.error(error)
            return False

    async def execute(self, query: str, args: tuple[Any, ...] = ()) -> bool:
        try:
            await self.pool.execute(query, args) if len(args) else await self.pool.executescript(query)
            await self.pool.commit()
            return True
        except Exception as error:
            self.logger.error(error)
            return False

    async def columns(self, tablename: str) -> list[str]:
        cursor: _aiosqlite.Cursor = await self.pool.execute(f'SELECT * FROM {tablename}')
        return list(map(lambda x: x[0], cursor.description))

    async def fetchall(self, query: str, args: tuple[Any, ...] = ()) -> list[MutableMapping]:
        try:
            cursor: _aiosqlite.Cursor = await self.pool.execute(query, args)
            result = [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in await cursor.fetchall()]
            await self.pool.commit()
            return result
        except Exception as error:
            self.logger.error(error)
            return []
