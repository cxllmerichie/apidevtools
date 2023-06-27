from typing import Any, Iterable

from ..types import Record
from ..connector import Connector


class Operation:
    connector: Connector
    _query: str
    _qargs: list

    def fr0m(self, table: str) -> 'Operation':
        c = self.connector.constraint_wrapper
        self._query += f"FROM {c}{table}{c} "
        return self

    def where(self, **conditions: Any) -> 'Operation':
        self._qargs += conditions.values()
        p, c = self.connector.placeholder, self.connector.constraint_wrapper
        conditions = ' AND '.join([f'{c}{key}{c} = {p}' for key, value in conditions.items()])
        self._query += f"WHERE {conditions} "
        return self

    def order(self, **columns: str) -> 'Operation':
        columns = ', '.join([f'{key} {value.upper()}' for key, value in columns.items()])
        self._query += f"ORDER BY {columns} "
        return self

    def limit(self, value: int) -> 'Operation':
        self._query += f"LIMIT {value} "
        return self

    def offset(self, value: int) -> 'Operation':
        self._query += f"OFFSET {value} "
        return self

    def returning(self, *columns, type: type = None) -> 'Operation':
        if type:
            ...
        if columns:
            self._query += f"RETURNING {', '.join(columns)} "
        return self

    def _refresh(self):
        self._qargs = []
        try:
            self.connector.placeholder_count = 0
        except AttributeError:
            ...

    async def all(self):
        print(self._query, self._qargs)
        return await self.connector.fetchall(self._query, tuple(self._qargs))
    #
    # async def first(self) -> Record:
    #     try:
    #         return await self._unwrap(self._records[0])
    #     except IndexError:
    #         return None
    #
    # async def last(self) -> Record:
    #     try:
    #         return await self._unwrap(self._records[-1])
    #     except IndexError:
    #         return None