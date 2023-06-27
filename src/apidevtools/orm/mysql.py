from typing import Any, MutableMapping, Optional, AsyncGenerator
from functools import cache
import aiomysql

from .types import CRUD, Connector
from .. import logman


class MySQL(Connector, CRUD):
    _placeholder = '%s'
    _constraint_wrapper = '`'
    _value_wrapper = '\''

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
            self.logger.info(f'`ORM.connector: {self.__class__.__name__}` pool created')
            return True
        except Exception as error:
            self.logger.error(error)
            return False

    async def close_pool(self) -> bool:
        try:
            self.pool.close()
            self.logger.info(f'`ORM.connector: {self.__class__.__name__}` pool closed')
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

    async def execute(self, query: str, args: tuple[Any, ...] = ())\
            -> bool:
        try:
            async with self.pool.acquire() as connection:
                async with connection.cursor(aiomysql.DictCursor) as cursor:
                    await cursor.execute(query, args)
                    await connection.commit()
                    return True
        except Exception as error:
            self.logger.error(error)
            return False

    async def fetchall(self, query: str, args: tuple[Any, ...] = (), type: type[dict] = dict)\
            -> list[MutableMapping]:
        try:
            async with self.pool.acquire() as connection:
                async with connection.cursor(aiomysql.DictCursor) as cursor:
                    await cursor.execute(query, args)
                    await connection.commit()
                    return await cursor.fetchall()
        except Exception as error:
            self.logger.error(error)
            return []

    async def fetchone(self, query: str, args: tuple[Any, ...] = (), type: type[dict] = dict)\
            -> Optional[MutableMapping]:
        try:
            async with self.pool.acquire() as connection:
                async with connection.cursor(aiomysql.DictCursor) as cursor:
                    await cursor.execute(query, args)
                    await connection.commit()
                    return await cursor.fetchone()
        except Exception as error:
            self.logger.error(error)
            return None

    async def rows(self, query: str, args: tuple[Any, ...] = (), type: type[dict] = dict)\
            -> AsyncGenerator[dict[str, Any], None]:
        async with self.pool.acquire() as connection:
            async with connection.cursor(aiomysql.DictCursor) as cursor:
                try:
                    await cursor.execute(query, args)
                    await connection.commit()
                    while True:
                        if item := await cursor.fetchone():
                            yield item
                        else:
                            break
                except Exception as error:
                    self.logger.error(error)
                    pass
