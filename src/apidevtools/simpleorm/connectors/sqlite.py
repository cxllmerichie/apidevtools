import aiosqlite
from loguru._logger import Logger
from typing import Any, MutableMapping
import loguru

from ..types import Relation
from ._connector import Connector


class SQLite(Connector):
    def __init__(self, database: str,
                 logger: Logger = loguru.logger):
        self.database: str = database if database.endswith('.sqlite') else f'{database}.sqlite'

        self.logger: Logger = logger

        self.pool: aiosqlite.Connection | None = None

    async def create_pool(self) -> bool:
        try:
            self.pool = await aiosqlite.connect(database=self.database)
        except Exception as error:
            self.logger.error(error)
            return False
        return True

    async def close_pool(self) -> bool:
        try:
            await self.pool.close()
        except Exception as error:
            self.logger.error(error)
            return False
        return True

    async def execute(self, query: str, args: tuple[Any, ...] = ()) -> Any:
        # self.pool.executescript accepts only query, can not accept args
        # used when no args passed, for cases like initializing db and creating tables on startup
        try:
            if len(args):
                cursor: aiosqlite.Cursor = await self.pool.execute(query, args)
            else:
                cursor: aiosqlite.Cursor = await self.pool.executescript(query)
            await self.pool.commit()
            return cursor.description
        except Exception as error:
            self.logger.error(error)

    async def columns(self, tablename: str) -> list[str]:
        cursor: aiosqlite.Cursor = await self.pool.execute(f'SELECT * FROM {tablename}')
        await self.pool.commit()
        return list(map(lambda x: x[0], cursor.description))

    async def fetchall(self, query: str, args: tuple[Any, ...] = ()) -> list[MutableMapping]:
        try:
            cursor: aiosqlite.Cursor = await self.pool.execute(query, args)
            result = [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in await cursor.fetchall()]
            await self.pool.commit()
            return result
        except Exception as error:
            self.logger.error(error)
        return []

    async def _constructor__select_relation(
            self, relation: Relation,
            *args, **kwargs
    ) -> tuple[str, tuple[Any, ...]]:
        return await super()._constructor__select_relation(relation, placeholder='?')

    async def _constructor__select_instance(
            self,
            instance: dict[str, Any], tablename: str,
            *args, **kwargs
    ) -> tuple[str, tuple[Any, ...]]:
        return await super()._constructor__select_instance(instance, tablename, placeholder='?')

    async def _constructor__insert_instance(
            self,
            instance: dict[str, Any], tablename: str,
            *args, **kwargs
    ) -> tuple[str, tuple[Any, ...]]:
        return await super()._constructor__insert_instance(instance, tablename, placeholder='?')

    async def _constructor__update_instance(
            self,
            instance: dict[str, Any], tablename: str, where: dict[str, Any],
            *args, **kwargs
    ) -> tuple[str, tuple[Any, ...]]:
        return await super()._constructor__update_instance(instance, tablename, where, placeholder='?')

    async def _constructor__delete_instance(
            self,
            instance: dict[str, Any], tablename: str,
            *args, **kwargs
    ) -> tuple[str, tuple[Any, ...]]:
        return await super()._constructor__delete_instance(instance, tablename, placeholder='?')
