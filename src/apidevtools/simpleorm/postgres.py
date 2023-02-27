from asyncpg.pool import create_pool as _create_pool, Pool as _Pool
from asyncpg.connection import Connection as _Connection
from asyncpg import exceptions as _exceptions
from loguru._logger import Logger
from typing import Any
import loguru

from .schema import Schema
from .records import Records
from .types import SchemaType, Record, Instance


class PostgreSQL:
    def __init__(self, database: str,
                 host: str = 'localhost', port: int | str = 5432,
                 user: str = 'postgres', password: str | None = None,
                 logger: Logger = loguru.logger):
        self.database: str = database
        self.host: str = host
        self.port: str | int = port
        self.user: str = user
        self.password: str | None = password

        self.logger: Logger = logger

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

    async def __aenter__(self) -> _Connection:
        try:
            self.__connection = await self.__pool.acquire()
            return self.__connection
        except AttributeError:
            self.logger.error('Attempting to create connection with not acquired pool')

    async def __aexit__(self, exc_type: Any, exc_value: Any, exc_traceback: Any) -> None:
        try:
            await self.__pool.release(self.__connection)
        except _exceptions.InterfaceError:
            self.logger.error('Attempting to release not acquired connection')

    async def execute(self, query: str, args: tuple[Any, ...] = ()) -> str:
        async with self as connection:
            return await connection.execute(query, *args)

    async def select(self, query: str, args: tuple[Any, ...] = (), schema_t: SchemaType = dict, depth: int = 0) -> Records:
        async with self as connection:
            records = Records(await connection.fetch(query, *args), schema_t)
        if depth > 0 and schema_t is not dict:
            for index, record in enumerate(records.all()):
                for relation in record.relations():
                    columns, values = ', '.join(relation.columns), tuple(relation.where.values())
                    conditions = ' AND '.join([f'"{key}" = ${index + 1}' for index, key in enumerate(relation.where.keys())])
                    query, args = f'SELECT {columns} FROM "{relation.tablename}" WHERE {conditions};', values
                    instances = (await self.select(query, args, relation.rel_schema_t, depth - 1)).all()
                    if isinstance(record, dict):
                        record[relation.fieldname] = instances
                    elif isinstance(record, Schema):
                        record = relation.ext_schema_t(**dict(record))
                        setattr(record, relation.fieldname, instances)
                    records.records[index] = relation.ext_schema_t(**dict(record))
        return records

    async def insert(self, instance: Instance, schema_t: SchemaType = dict, tablename: str = None) -> Record:
        instance, tablename = await self.__parse_parameters(instance, tablename)
        placeholders = ', '.join([f'${index + 1}' for index in range(len(instance.keys()))])
        columns, values = str(tuple(instance.keys())).replace("'", '"'), instance.values()
        query, args = f'INSERT INTO "{tablename}" {columns} VALUES ({placeholders}) RETURNING *;', values
        async with self as connection:
            records = await connection.fetch(query, *args)
        return Records(records, schema_t).first()

    async def update(self, instance: Instance, where: dict[str, Any], schema_t: SchemaType = dict, tablename: str = None) -> Records:
        instance, tablename = await self.__parse_parameters(instance, tablename)
        values = ', '.join([f'"{key}" = ${index + 1}' for index, key in enumerate(instance.keys())])
        conditions = ' AND '.join([f'"{key}" = \'{value}\'' for key, value in where.items()])
        query, args = f'UPDATE "{tablename}" SET {values} WHERE {conditions} RETURNING *;', tuple(instance.values())
        async with self as connection:
            records = await connection.fetch(query, *args)
        return Records(records, schema_t)

    async def delete(self, instance: Instance, schema_t: SchemaType = dict, tablename: str = None) -> Records:
        # Method successfully removes the instance from the database. Supposed to return the instance and all
        # related to it instances (children relations), but returns only the instance itself, because of the issue below
        instance, tablename = await self.__parse_parameters(instance, tablename)
        conditions = ' AND '.join([f'"{key}" = ${index + 1}' for index, key in enumerate(instance.keys())])
        query, args = f'SELECT * FROM "{tablename}" WHERE {conditions};', tuple(instance.values())
        # ISSUE 1:
        #   attaching removed relational children to this "records"
        records = await self.select(query, args, schema_t)
        for index, record in enumerate(records.all()) if schema_t is not dict else ():
            for relation in record.relations():
                instances = (await self.delete(dict(**relation.where), relation.rel_schema_t, relation.tablename)).all()
                if isinstance(record, dict):
                    record[relation.fieldname] = instances
                elif isinstance(record, Schema):
                    record = relation.ext_schema_t(**dict(record))
                    setattr(record, relation.fieldname, instances)
                records.records[index] = relation.ext_schema_t(**dict(record))
        query, args = f'DELETE FROM "{tablename}" WHERE {conditions} RETURNING *;', tuple(instance.values())
        async with self as connection:
            records = await connection.fetch(query, *args)
        # ISSUE 1 (continuation):
        #   but returning another records
        return Records(records, schema_t)

    async def __parse_instance(self, instance: dict[str, Any], tablename: str) -> tuple[tuple[str, ...], tuple[str, ...]]:
        query, args = 'SELECT "column_name" FROM information_schema.columns WHERE "table_name" = $1;', (tablename,)
        async with self as connection:
            db_columns = [record['column_name'] for record in Records(await connection.fetch(query, *args)).all()]
        instance_columns = set(instance.keys())
        columns = instance_columns.intersection(db_columns)
        for key in instance_columns.difference(db_columns):
            if key not in columns:
                instance.pop(key)
        return tuple(columns), tuple([instance[column] for column in columns])

    async def __parse_parameters(self, instance: Instance, tablename: str) -> tuple[Record, str]:
        if isinstance(instance, Schema):
            tablename = instance.tablename
            instance = dict(instance.into_db())
        if not tablename:
            raise AttributeError('Specify "tablename" if "instance" is a "dict" type, otherwise pass '
                                 '"Schema" type object with overwritten property "__tablename__"')
        await self.__parse_instance(instance, tablename)
        return instance, tablename
