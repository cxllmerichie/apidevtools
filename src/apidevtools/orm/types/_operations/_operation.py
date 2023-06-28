from typing import Any, Iterable, Optional

from ..types import RecordType, Record


class Operation:
    _query: str
    _qargs: list
    _type: type

    def fr0m(self, table: str) -> 'Operation':
        c = self._constraint_wrapper
        self._query += f"FROM {c}{table}{c} "
        return self

    def where(self, **conditions: Any) -> 'Operation':
        self._qargs += conditions.values()
        p, c = self._placeholder, self._constraint_wrapper
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

    def returning(self, *columns, type: RecordType = dict) -> 'Operation':
        if type:
            self._type = type
        if columns:
            self._query += f"RETURNING {', '.join(columns)} "
        return self

    async def all(self, type: RecordType = dict) -> list[Record]:
        if not (query := self._query.lower()).startswith('select'):
            if 'returning' not in query:
                self.returning('*')
        return await self.fetchall(f'{self._query[:-1]};', tuple(self._qargs), type)

    async def one(self, type: RecordType = dict) -> Optional[Record]:
        if not (query := self._query.lower()).startswith('select'):
            if 'returning' not in query:
                self.returning('*')
        return await self.fetchone(f'{self._query[:-1]};', tuple(self._qargs), type)

    async def exec(self) -> bool:
        return await self.execute(f'{self._query[:-1]};', tuple(self._qargs))

    def _refresh(self):
        self._qargs = []
        self._type = dict
        try:
            self._placeholder_count = 0
        except AttributeError:
            ...


Query: type = type[str | Operation]
