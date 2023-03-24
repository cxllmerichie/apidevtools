from loguru._logger import Logger
from typing import Any
import loguru
from apidevtools import INF

from .types import RecordType, Record, Schema, Records
from .connectors._connector import Connector


Instance = dict[str, Any] | Schema


class ORM:
    def __init__(self, connector: Connector, logger: Logger = loguru.logger):
        self.connector: Connector = connector
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

    async def select(
            self,
            query: str, args: tuple[Any, ...] = (), record_t: RecordType = dict[str, Any],
            *, rel_depth: int = 0
    ) -> Records:
        records = Records(await self.connector.fetchall(query, args), record_t)
        for index, record in enumerate(records.all()) if record_t is not dict else ():
            if rel_depth == 0:
                break
            for relation in record.relations():
                query, args = await self.connector._constructor__select_relations(relation)
                instances = (await self.select(query, args, relation.rel_schema_t, rel_depth=rel_depth - 1)).all()
                if isinstance(record, dict):
                    record[relation.propname] = instances
                elif isinstance(record, Schema):
                    record = relation.ext_schema_t(**dict(record))
                    setattr(record, relation.propname, instances)
                records._records[index] = relation.ext_schema_t(**dict(record))
        return records

    async def insert(
            self,
            instance: Instance, record_t: RecordType = dict[str, Any], tablename: str = None
    ) -> Record:
        instance, tablename = await self.__parse_parameters(instance, tablename)
        query, args = await self.connector._constructor__insert_instance(instance, tablename)
        return Records(await self.connector.fetchall(query, args), record_t).first()

    async def update(
            self,
            instance: Instance, where: dict[str, Any], record_t: RecordType = dict[str, Any], tablename: str = None
    ) -> Records:
        instance, tablename = await self.__parse_parameters(instance, tablename)
        query, args = await self.connector._constructor__update_instances(instance, tablename, where)
        return Records(await self.connector.fetchall(query, args), record_t)

    async def delete(
            self,
            instance: Instance, record_t: RecordType = dict[str, Any], tablename: str = None,
            *, rel_depth: int = 0, del_depth: int = INF
    ) -> Records:
        instance, tablename = await self.__parse_parameters(instance, tablename)
        query, args = await self.connector._constructor__select_instances(instance, tablename)
        records = await self.select(query, args, record_t)
        for index, record in enumerate(records.all()) if record_t is not dict else ():
            if del_depth == 0:
                break
            for relation in record.relations():
                instances = (await self.delete(relation.where, relation.rel_schema_t, relation.rel_schema_t.__tablename__, del_depth=del_depth - 1)).all()
                if rel_depth == 0:
                    break
                if isinstance(record, dict):
                    record[relation.propname] = instances
                elif isinstance(record, Schema):
                    record = relation.ext_schema_t(**dict(record))
                    setattr(record, relation.propname, instances)
                records._records[index] = relation.ext_schema_t(**dict(record))
        await self.connector.execute(*(await self.connector._constructor__delete_instances(instance, tablename)))
        return records

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
