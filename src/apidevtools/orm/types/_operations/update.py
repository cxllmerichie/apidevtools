from typing import Any

from ._operation import Operation
from ..types import Schema, Record


class Update(Operation):
    def update(self, table: str, instance: Record = None) -> 'Update':
        self._refresh()
        if instance:
            if isinstance(instance, Schema):
                self.update(instance.__tablename__)
                self.set(**dict(instance))
                key = instance.__primary__
                self.where(**{key: instance.__getattribute__(key)})
            return self
        self._query = f"UPDATE {table} "
        return self

    def set(self, **values: Any) -> 'Update':
        self._qargs += values.values()
        p, c = self._placeholder, self._constraint_wrapper  # noqa
        values = ', '.join([f'{c}{key}{c} = {p}' for key, value in values.items()])
        self._query += f"SET {values} "
        return self
