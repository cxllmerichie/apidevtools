from ._operation import Operation


class Delete(Operation):
    def delete(self, instance=None) -> 'Delete':
        self._refresh()

        if instance:
            ...
        self._query = 'DELETE '
        return self
    