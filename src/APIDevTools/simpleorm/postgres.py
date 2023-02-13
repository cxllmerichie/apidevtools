from typing import Any
from asyncpg.pool import create_pool as _create_pool, Pool as _Pool
from asyncpg.connection import Connection as _Connection
from asyncpg import exceptions as _exceptions
from loguru._logger import Logger
import loguru

from .schema import Schema
from .records import Records
from .base import BaseStorage


class PostgresqlStorage(BaseStorage):
    def __init__(self, database: str,
                 host: str = 'localhost', port: str | int = 5432,
                 user: str = 'postgres', password: str | None = None,
                 logger: Logger = loguru.logger):
        super().__init__(database, host, port, user, password, logger)

        self.__pool: _Pool | None = None
        self.__connection: _Connection | None = None

    async def create_pool(self) -> bool:
        try:
            self.__pool = await _create_pool(database=self.database, host=self.host, port=self.port, user=self.user, password=self.password)
        except OSError:
            self.logger.error('Pool creation failed')
        return self.__pool is not None

    async def close_pool(self) -> bool:
        try:
            await self.__pool.expire_connections()
            await self.__pool.close()
            return True
        except AttributeError:
            self.logger.error(f'Attempting to close not acquired pool')
        return False

    async def __aenter__(self):
        try:
            self.__connection = await self.__pool.acquire()
            return self.__connection
        except AttributeError:
            self.logger.error('Attempting to create connection with not acquired pool')

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        try:
            await self.__pool.release(self.__connection)
        except _exceptions.InterfaceError:
            self.logger.error('Attempting to release not acquired connection')

    async def execute(self, query: str, args: tuple[Any, ...] = ()) -> Any:
        async with self as connection:
            return await connection.execute(query, *args)

    async def select(self, query: str, args: tuple[Any, ...] = (), schema_t: type = None, depth: int = 0) -> Records:
        async with self as connection:
            records = await connection.fetch(query, *args)
        records = Records(records, schema_t)
        if not depth:
            for index, record in enumerate(records.all()):
                for relation in record.relations():
                    columns = ', '.join([f'"{column}"' if column != '*' else '*' for column in relation.columns])
                    conditions = ' and '.join(
                        [f'"{key}" = ${index + 1}' for index, key in enumerate(list(relation.where.keys()))])
                    query, args = f'SELECT {columns} FROM "{relation.tablename}" WHERE {conditions};', tuple(
                        relation.where.values())
                    instances = (await self.select(query, args, relation.rel_schema_t, depth - 1)).all()
                    if isinstance(record, dict):
                        record[relation.fieldname] = instances
                    elif isinstance(record, schema_t):
                        record = relation.ext_schema_t(**dict(record))
                        setattr(record, relation.fieldname, instances)
                    records.records[index] = relation.ext_schema_t(**dict(record))
        return records

    async def insert(self, schema: Schema, schema_t: type = None) -> Schema | dict[str, Any] | None:
        data = dict(schema.pretty())
        placeholders = ', '.join([f'${index + 1}' for index in range(len(data.keys()))])
        columns, values = str(tuple(data.keys())).replace("'", '"'), data.values()
        query, args = f'INSERT INTO "{schema.tablename}" {columns} VALUES ({placeholders}) RETURNING *;', values
        async with self as connection:
            records = await connection.fetch(query, *args)
        return Records(records, schema_t).first()

    async def update(self, schema: Schema, where: dict[str, Any], schema_t: type = None) -> Schema | dict[str, Any] | None:
        data = dict(schema.pretty())
        values = ', '.join([f'"{key}" = ${index + 1}' for index, key in enumerate(data.keys())])
        conditions = ' and '.join([f'"{key}" = \'{value}\'' for key, value in where.items()])
        query, args = f'UPDATE "{schema.tablename}" SET {values} WHERE {conditions} RETURNING *;', tuple(data.values())
        async with self as connection:
            records = await connection.fetch(query, *args)
        return Records(records, schema_t).first()
