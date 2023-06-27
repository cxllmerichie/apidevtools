import aiomysql as _aiomysql
from typing import Any, MutableMapping

from ..types import Relation
from ._connector import Connector
from ... import logman


class MySQL(Connector):
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
        self.pool: _aiomysql.Pool | None = None

        super().__init__(placeholder='%s', constraint_wrapper='`', value_wrapper="'")

    async def create_pool(self) -> bool:
        try:
            self.pool = await _aiomysql.create_pool(
                db=self.database, host=self.host, port=self.port, user=self.user, password=self.password
            )
            return True
        except Exception as error:
            self.logger.error(error)
            return False

    async def close_pool(self) -> bool:
        try:
            self.pool.close()
            return True
        except Exception as error:
            self.logger.error(error)
            return False

    async def execute(self, query: str, args: tuple[Any, ...] = ()) -> bool:
        try:
            async with self.pool.acquire() as connection:
                async with connection.cursor(_aiomysql.DictCursor) as cursor:
                    await cursor.execute(query, args)
                    await connection.commit()
                    return True
        except Exception as error:
            self.logger.error(error)
            return False

    async def columns(self, tablename: str) -> list[str]:
        query, args = 'SELECT `COLUMN_NAME` FROM `INFORMATION_SCHEMA`.`COLUMNS` WHERE `TABLE_SCHEMA` = %s AND `TABLE_NAME` = %s;', (self.database, tablename)
        async with self.pool.acquire() as connection:
            async with connection.cursor(_aiomysql.DictCursor) as cursor:
                await cursor.execute(query, args)
                await connection.commit()
                return [record['COLUMN_NAME'] for record in await cursor.fetchall()]

    async def fetchall(self, query: str, args: tuple[Any, ...] = ()) -> list[MutableMapping]:
        try:
            async with self.pool.acquire() as connection:
                async with connection.cursor(_aiomysql.DictCursor) as cursor:
                    await cursor.execute(query, args)
                    await connection.commit()
                    return await cursor.fetchall()
        except Exception as error:
            self.logger.error(error)
            return []
