from typing import Any

from ._operation import Operation


class Select(Operation):
    def select(self, *columns: str) -> 'Select':
        c = self._constraint_wrapper  # noqa
        columns = ', '.join([f'{c}{column}{c}' for column in columns])
        self._commands['select'] = f"SELECT {columns}"
        return self
