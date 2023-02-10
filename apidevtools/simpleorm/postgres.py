from typing import Any
from asyncpg.pool import create_pool, Pool
from asyncpg.connection import Connection
from asyncpg import exceptions
from loguru._logger import Logger
import loguru

from apidevtools.simpleorm.schema import Schema
from apidevtools.simpleorm.records import Records
from .base import BaseStorage
from apidevtools.simpleorm.relation import Relation


class PostgresqlStorage(BaseStorage):
    def __init__(self, database: str,
                 host: str = 'localhost', port: str | int = 5432,
                 user: str = 'postgres', password: str | None = None,
                 logger: Logger = loguru.logger):
        super().__init__(database, host, port, user, password, logger)

        self.__pool: Pool | None = None
        self.__connection: Connection | None = None

    async def create_pool(self) -> bool:
        try:
            self.__pool = await create_pool(database=self.database, host=self.host, port=self.port, user=self.user, password=self.password)
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
        except exceptions.InterfaceError:
            self.logger.error('Attempting to release not acquired connection')

    async def execute(self, query: str, args: tuple[Any, ...] = ()) -> Any:
        async with self as connection:
            return await connection.execute(query, *args)

    async def select(self, query: str, args: tuple[Any, ...] = (), schema_t: type = None, relations: list[Relation] = None) -> Records:
        async with self as connection:
            records = await connection.fetch(query, *args)
        records = Records(records, schema_t)
        if relations:
            for relation in relations:
                for index, record in enumerate(records.all()):
                    columns = ', '.join([f'"{column}"' for column in relation.columns])
                    conditions = ' and '.join([f'"{key}" = ${index}' for index, key in enumerate(list(relation.where.items()))])
                    query, args = f'SELECT {columns} FROM "{relation.tablename}" WHERE {conditions};', tuple(relation.where.values())
                    instances = (await self.select(query, args, relation.rel_schema_t)).all()
                    if isinstance(record, dict):
                        record[relation.fieldname] = instances
                    elif isinstance(record, schema_t):
                        record = relation.ext_schema_t(**dict(record))
                        setattr(record, relation.fieldname, instances)
                    elif isinstance(record, relation.ext_schema_t):
                        records.__records[index] = relation.ext_schema_t(**dict(record))
        return records

    async def insert(self, schema: Schema, schema_t: type = None) -> Schema | dict[str, Any] | None:
        data = dict(schema.pretty())
        psql_placeholders = ', '.join([f'${index + 1}' for index in range(len(data.keys()))])
        columns, values = str(tuple(data.keys())).replace("'", '"'), data.values()
        query, args = f'INSERT INTO "{schema.tablename}" {columns} VALUES ({psql_placeholders}) RETURNING *;', values
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