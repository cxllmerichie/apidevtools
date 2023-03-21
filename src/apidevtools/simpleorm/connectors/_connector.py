from abc import ABC, abstractmethod
from typing import Any, MutableMapping

from ..types import Relation


class Connector(ABC):
    @abstractmethod
    def __init__(self, database: str, host: str, port: int | str, user: str, password: str | None):
        ...

    @abstractmethod
    async def create_pool(self) -> bool:
        ...

    @abstractmethod
    async def close_pool(self) -> bool:
        ...

    @abstractmethod
    async def execute(self, query: str, args: tuple[Any, ...] = ()) -> Any:
        ...

    @abstractmethod
    async def columns(self, tablename: str) -> list[str]:
        ...

    @abstractmethod
    async def fetchall(self, query: str, args: tuple[Any, ...] = ()) -> list[MutableMapping]:
        ...

    @abstractmethod
    async def _constructor__select_relation(
            self, relation: Relation,
            *, placeholder: str = '%s'
    ) -> tuple[str, tuple[Any, ...]]:
        columns, values = ', '.join(relation.columns), tuple(relation.where.values())
        conditions = ' AND '.join([f'"{key}" = {placeholder}' for key in relation.where.keys()])
        return f'SELECT {columns} FROM "{relation.tablename}" WHERE {conditions};', values

    @abstractmethod
    async def _constructor__select_instance(
            self,
            instance: dict, tablename: str,
            *, placeholder: str = '%s'
    ) -> tuple[str, tuple[Any, ...]]:
        conditions = ' AND '.join([f'"{key}" = {placeholder}' for key in instance.keys()])
        return f'SELECT * FROM "{tablename}" WHERE {conditions};', tuple(instance.values())

    @abstractmethod
    async def _constructor__insert_instance(
            self,
            instance: dict, tablename: str,
            *, placeholder: str = '%s'
    ) -> tuple[str, tuple[Any, ...]]:
        placeholders = ', '.join([placeholder for _ in range(len(instance.keys()))])
        columns, values = str(tuple(instance.keys())).replace("'", '"'), tuple(instance.values())
        return f'INSERT INTO "{tablename}" {columns} VALUES ({placeholders}) RETURNING *;', values

    @abstractmethod
    async def _constructor__update_instance(
            self,
            instance: dict, tablename: str, where: dict[str, Any],
            *, placeholder: str = '%s'
    ) -> tuple[str, tuple[Any, ...]]:
        values = ', '.join([f'{key} = {placeholder}' for key in instance.keys()])
        conditions = ' AND '.join([f'"{key}" = \'{value}\'' for key, value in where.items()])
        return f'UPDATE "{tablename}" SET {values} WHERE {conditions} RETURNING *;', tuple(instance.values())

    @abstractmethod
    async def _constructor__delete_instance(
            self,
            instance: dict, tablename: str,
            *, placeholder: str = '%s'
    ) -> tuple[str, tuple[Any, ...]]:
        conditions = ' AND '.join([f'"{key}" = {placeholder}' for key in instance.keys()])
        return f'DELETE FROM "{tablename}" WHERE {conditions} RETURNING *;', tuple(instance.values())
