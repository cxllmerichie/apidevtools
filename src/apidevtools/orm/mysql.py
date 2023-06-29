from typing import Any, Optional, AsyncGenerator, Callable, Awaitable
from functools import cache
import aiomysql

from .types import Connector, RecordType, Record, Insert, Select, Update, Delete, Query, Schema
from .. import logman


class MySQL(Connector, Insert, Select, Update, Delete):
    _placeholder = '%s'

    def __init__(self, database: str,
                 host: str = 'localhost', port: int | str = 3306,
                 user: str = 'root', password: str | None = None,
                 logger: logman.Logger = logman.logger):
        self.database: str = database
        self.host: str = host
        self.port: str | int = port
        self.user: str = user
        self.password: str | None = password

        self.logger: logman.Logger = logger
        self.pool: aiomysql.Pool | None = None

    async def create_pool(self) -> bool:
        try:
            self.pool = await aiomysql.create_pool(
                db=self.database, host=self.host, port=self.port, user=self.user, password=self.password
            )
            self.logger.info(f'{self.__class__.__name__} pool created')
            return True
        except Exception as error:
            self.logger.error(error)
            return False

    async def close_pool(self) -> bool:
        try:
            self.pool.close()
            self.logger.info(f'{self.__class__.__name__} pool closed')
            return True
        except Exception as error:
            self.logger.error(error)
            return False

    # @cache
    # async def columns(self, tablename: str) -> list[str]:
    #     query, args = 'SELECT `COLUMN_NAME` FROM `INFORMATION_SCHEMA`.`COLUMNS` WHERE `TABLE_SCHEMA` = %s AND `TABLE_NAME` = %s;', (self.database, tablename)
    #     async with self.pool.acquire() as connection:
    #         async with connection.cursor(aiomysql.DictCursor) as cursor:
    #             await cursor.execute(query, args)
    #             await connection.commit()
    #             return [record['COLUMN_NAME'] for record in await cursor.fetchall()]

    async def execute(self, query: Query, args: tuple[Any, ...] = ()) -> bool:
        query, args, _, _ = await self._parameters(query, args, None)
        try:
            async with self.pool.acquire() as connection:
                async with connection.cursor(aiomysql.DictCursor) as cursor:
                    await cursor.execute(query, args)
                    await connection.commit()
                    return True
        except Exception as error:
            self.logger.error(error)
            return False

    async def fetchone(self, query: Query, args: tuple[Any, ...] = (), type: RecordType = dict) -> Optional[Record]:
        query, args, type, unwrap = await self._parameters(query, args, type)
        try:
            async with self.pool.acquire() as connection:
                async with connection.cursor(aiomysql.DictCursor) as cursor:
                    await cursor.execute(query, args)
                    await connection.commit()
                    if record := await cursor.fetchone():
                        return await unwrap(record, type)
        except Exception as error:
            self.logger.error(error)
            return None

    async def records(self, query: Query, args: tuple[Any, ...] = (), type: RecordType = dict) -> AsyncGenerator[Record, None]:
        query, args, type, unwrap = await self._parameters(query, args, type)
        try:
            async with self.pool.acquire() as connection:
                async with connection.cursor(aiomysql.DictCursor) as cursor:
                    await cursor.execute(query, args)
                    await connection.commit()
                    while record := await cursor.fetchone():
                        yield await unwrap(record, type)
        except Exception as error:
            self.logger.error(error)

    def _unwrapper(self, type: RecordType) -> Callable[[Any, RecordType], Awaitable[Record]]:
        async def to_dict(record: Any, _: RecordType) -> dict[str, Any]:
            return record

        async def to_schema(record: Any, type: RecordType) -> Schema:
            return await type(**record).from_db()

        return to_dict if type is dict else to_schema
