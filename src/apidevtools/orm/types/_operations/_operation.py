from typing import Any, Optional

from ..types import RecordType, Record


class Operation:
    _mapping: dict[str, int] = {
        'insert': 1, 'select': 1, 'update': 1, 'delete': 1,
        'from': 2, 'into': 2,
        'columns': 3,
        'values': 4, 'set': 4,
        'where': 5,
        'order': 6,
        'limit': 7,
        'offset': 8,
        'returning': 9,
    }
    _commands: dict[str, str] = {}
    _args: list = []
    _type: type = dict

    def fr0m(self, table: str) -> 'Operation':
        c = self._constraint_wrapper  # noqa

        self._commands['from'] = f"FROM {c}{table}{c}"
        return self

    def where(self, **conditions: Any) -> 'Operation':
        self._args += conditions.values()
        p, c = self._placeholder, self._constraint_wrapper  # noqa
        conditions = ' AND '.join([f'{c}{key}{c} = {p}' for key, value in conditions.items()])
        self._commands['where'] = f"WHERE {conditions}"
        return self

    def order(self, **columns: str) -> 'Operation':
        columns = ', '.join([f'{key} {value.upper()}' for key, value in columns.items()])
        self._commands['order'] = f"ORDER BY {columns}"
        return self

    def limit(self, value: int) -> 'Operation':
        self._commands['limit'] = f"LIMIT {value}"
        return self

    def offset(self, value: int) -> 'Operation':
        self._commands['offset'] = f"OFFSET {value}"
        return self

    def returning(self, *columns, type: RecordType = dict) -> 'Operation':
        if type:
            self._type = type
        if columns:
            self._commands['returning'] = f"RETURNING {', '.join(columns)}"
        return self

    async def all(self, type: RecordType = dict) -> list[Record]:
        return await self.fetchall(self, self._args, type)  # noqa

    async def one(self, type: RecordType = dict) -> Optional[Record]:
        return await self.fetchone(self, self._args, type)  # noqa

    async def exec(self) -> bool:
        return await self.execute(self, self._args)  # noqa


Query: type = type[str, Operation]
