from loguru._logger import Logger
from typing import Any
import loguru

from .types import SchemaType, Record, Schema, Records
from .connector._base import SQLConnector


Instance = dict[str, Any] | Schema


class ORM:
    def __init__(self, connector: SQLConnector, logger: Logger = loguru.logger):
        self.connector: SQLConnector = connector
        self.logger: Logger = logger

    async def create_pool(self) -> bool:
        try:
            return await self.connector.create_pool()
        except Exception as error:
            self.logger.error(error)
            return False

    async def close_pool(self) -> bool:
        try:
            return await self.connector.close_pool()
        except Exception as error:
            self.logger.error(f'{error}')
            return False

    async def execute(self, query: str, args: tuple[Any, ...] = ()) -> Any:
        return await self.connector.execute(query, args)

    async def select(self, query: str, args: tuple[Any, ...] = (), schema_t: SchemaType = dict, depth: int = 0)\
            -> Records:
        records = Records(await self.connector.fetchall(query, args), schema_t)
        if depth > 0 and schema_t is not dict:
            for index, record in enumerate(records.all()):
                for relation in record.relations():
                    query, args = self.connector.constructor__select_relation(relation)
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
        query, args = await self.connector.constructor__insert_instance(instance, tablename)
        return Records(await self.connector.fetchall(query, args), schema_t).first()

    async def update(self, instance: Instance, where: dict[str, Any], schema_t: SchemaType = dict, tablename: str = None)\
            -> Records:
        instance, tablename = await self.__parse_parameters(instance, tablename)
        query, args = await self.connector.constructor__update_instance(instance, tablename, where)
        return Records(await self.connector.fetchall(query, args), schema_t)

    async def delete(self, instance: Instance, schema_t: SchemaType = dict, tablename: str = None) -> Records:
        # Method successfully removes the instance from the database. Supposed to return the instance and all
        # related to it instances (children relations), but returns only the instance itself, because of the issue below
        instance, tablename = await self.__parse_parameters(instance, tablename)
        query, args = self.connector.constructor__select_instance(instance, tablename)
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
        query, args = await self.connector.constructor__delete_instance(instance, tablename)
        # ISSUE 1 (continuation):
        #   but returning another records
        return Records(await self.connector.fetchall(query, args), schema_t)

    async def __parse_instance(self, instance: dict[str, Any], tablename: str)\
            -> tuple[tuple[str, ...], tuple[str, ...]]:
        db_columns = await self.connector.columns(tablename)
        instance_columns = set(instance.keys())
        columns = instance_columns.intersection(db_columns)
        for key in instance_columns.difference(db_columns):
            if key not in columns:
                instance.pop(key)
        return tuple(columns), tuple([instance[column] for column in columns])

    async def __parse_parameters(self, instance: Instance, tablename: str) -> tuple[Record, str]:
        if isinstance(instance, Schema):
            tablename = instance.__tablename__
            instance = dict(instance.into_db())
        if not tablename:
            raise AttributeError('Specify "tablename" if "instance" is a "dict", otherwise pass "Schema" object')
        await self.__parse_instance(instance, tablename)
        return instance, tablename
