from ._operation import Operation


class Delete(Operation):
    def __init__(self, instance=None):
        self._refresh()

        if instance:
            ...
        self._query = 'DELETE '
