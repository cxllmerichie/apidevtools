from typing import Any
from asyncpg.pool import create_pool as _create_pool, Pool as _Pool
from asyncpg.connection import Connection as _Connection
from asyncpg import exceptions as _exceptions
from loguru._logger import Logger
import loguru

from .schema import Schema
from .records import Records
from .base import BaseORM
from .types import SchemaType, Record, Instance


class PostgreSQL(BaseORM):
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

    async def select(self, query: str, args: tuple[Any, ...] = (), schema_t: SchemaType = dict, depth: int = 0) -> Records:
        async with self as connection:
            records = await connection.fetch(query, *args)
        records = Records(records, schema_t)
        if depth > 0 and schema_t is not dict:
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
                    elif isinstance(record, Schema):
                        record = relation.ext_schema_t(**dict(record))
                        setattr(record, relation.fieldname, instances)
                    records.records[index] = relation.ext_schema_t(**dict(record))
        return records

    async def insert(self, instance: Instance, schema_t: SchemaType = dict, tablename: str = None) -> Record:
        instance, tablename = self.__parse_params(instance, tablename)
        placeholders = ', '.join([f'${index + 1}' for index in range(len(instance.keys()))])
        columns, values = str(tuple(instance.keys())).replace("'", '"'), instance.values()
        query, args = f'INSERT INTO "{tablename}" {columns} VALUES ({placeholders}) RETURNING *;', values
        async with self as connection:
            records = await connection.fetch(query, *args)
        return Records(records, schema_t).first()

    async def update(self, instance: Instance, where: dict[str, Any], schema_t: SchemaType = dict, tablename: str = None) -> Record:
        instance, tablename = self.__parse_params(instance, tablename)
        values = ', '.join([f'"{key}" = ${index + 1}' for index, key in enumerate(instance.keys())])
        conditions = ' and '.join([f'"{key}" = \'{value}\'' for key, value in where.items()])
        query, args = f'UPDATE "{tablename}" SET {values} WHERE {conditions} RETURNING *;', tuple(instance.values())
        async with self as connection:
            records = await connection.fetch(query, *args)
        return Records(records, schema_t).first()

    async def delete(self, instance: Instance, schema_t: SchemaType = dict, tablename: str = None) -> Record:
        instance, tablename = self.__parse_params(instance, tablename)
        outer_conditions = ' and '.join([f'"{key}" = ${index + 1}' for index, key in enumerate(instance.keys())])
        query, args = f'SELECT * FROM "{tablename}" WHERE {outer_conditions};', tuple(instance.values())
        records = await self.select(query, args, schema_t)
        for index, record in enumerate(records.all()):
            if schema_t is dict:
                break
            for relation in record.relations():
                columns = ', '.join([f'"{column}"' if column != '*' else '*' for column in relation.columns])
                conditions = ' and '.join([f'"{key}" = ${index + 1}' for index, key in enumerate(list(relation.where.keys()))])
                query, args = f'SELECT {columns} FROM "{relation.tablename}" WHERE {conditions};', tuple(relation.where.values())
                instances = (await self.select(query, args, relation.rel_schema_t, 1)).all()
                for inst in instances:
                    await self.delete(inst, relation.rel_schema_t)
                if isinstance(record, dict):
                    record[relation.fieldname] = instances
                elif isinstance(record, Schema):
                    record = relation.ext_schema_t(**dict(record))
                    setattr(record, relation.fieldname, instances)
                records.records[index] = relation.ext_schema_t(**dict(record))
        query, args = f'DELETE FROM "{tablename}" WHERE {outer_conditions};', tuple(instance.values())
        async with self as connection:
            await connection.fetch(query, *args)
        return records.first()

    def __parse_params(self, instance: Instance, tablename: str) -> tuple[Record, str]:
        if isinstance(instance, Schema):
            tablename = instance.tablename
            instance = dict(instance.pretty())
        if not tablename and isinstance(instance, dict):
            raise AttributeError('Please specify "tablename" parameter if "instance" has a "dict" type'
                                 ' or pass "Schema" type object with overwritten property "tablename"')
        return instance, tablename
