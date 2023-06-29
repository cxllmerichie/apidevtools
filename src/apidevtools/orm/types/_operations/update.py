from typing import Any

from ._operation import Operation
from ..types import Schema, Record


class Update(Operation):
    def update(self, what: Record | str) -> 'Update':
        self._refresh()
        if isinstance(what, Schema):
            self.update(what.__tablename__)
            self.set(**dict(what))
            key = what.__primary__
            self.where(**{key: what.__getattribute__(key)})
        elif isinstance(what, dict):
            ...
        elif isinstance(what, str):
            self._query = f"UPDATE {what} "
        return self

    def set(self, **values: Any) -> 'Update':
        self._qargs += values.values()
        p, c = self._placeholder, self._constraint_wrapper  # noqa
        values = ', '.join([f'{c}{key}{c} = {p}' for key, value in values.items()])
        self._query += f"SET {values} "
        return self
