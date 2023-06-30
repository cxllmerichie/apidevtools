from typing import Any
from contextlib import suppress

from ._operation import Operation
from ..types import Schema


class Update(Operation):
    def update(self, what: Schema | str) -> 'Update':
        if isinstance(what, Schema):
            self._commands['update'] = f"UPDATE {what.__tablename__}"
            self.set(**{key: value for key, value in dict(what).items() if key != (primary := what.__primary__)})
            with suppress(AttributeError):
                self.where(**{primary: what.__getattribute__(primary)})
        elif isinstance(what, str):
            self._commands['update'] = f"UPDATE {what}"
        return self

    def set(self, **values: Any) -> 'Update':
        self._args += values.values()
        p, c = self._placeholder, self._constraint_wrapper  # noqa
        values = ', '.join([f'{c}{key}{c} = {p}' for key, value in values.items()])
        self._commands['set'] = f"SET {values}"
        return self
