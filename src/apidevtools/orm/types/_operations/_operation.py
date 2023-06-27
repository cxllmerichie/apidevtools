from typing import Any, Iterable

# from src.apidevtools.orm.types import Schema


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

    # def returning(self, *columns, type: type[dict | Schema] = dict) -> 'Operation':
    def returning(self, *columns, type: type[dict] = dict) -> 'Operation':
        if type:
            self._type = type
        if columns:
            self._query += f"RETURNING {', '.join(columns)} "
        return self

    def _refresh(self):
        self._qargs = []
        self._type = dict
        try:
            self._placeholder_count = 0
        except AttributeError:
            ...

    def __enter__(self):
        return self.rows(self._query, self._qargs, self._type)

    def __exit__(self, exc_type, exc_val, exc_tb):
        ...

    async def all(self, type: type[dict] = dict):
        if not (query := self._query.lower()).startswith('select'):
            if 'returning' not in query:
                self.returning('*')
        return await self.fetchall(f'{self._query[:-1]};', tuple(self._qargs), type)

    async def one(self, type: type[dict] = dict):
        if not (query := self._query.lower()).startswith('select'):
            if 'returning' not in query:
                self.returning('*')
        return await self.fetchone(f'{self._query[:-1]};', tuple(self._qargs), type)

    async def exec(self):
        return await self.execute(f'{self._query[:-1]};', tuple(self._qargs))

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