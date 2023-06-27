from ._crud import Select, Delete, Insert, Update
from .connector import Connector
from .. import logman


class ORM:
    def __init__(self, connector: Connector, logger: logman.Logger = logman.logger):
        self.connector: Connector = connector
        self.logger: logman.Logger = logger

    async def create_pool(self) -> bool:
        try:
            is_created = await self.connector.create_pool()
            self.logger.info(f'`ORM.connector: {self.connector.__class__.__name__}` pool created')
            return is_created
        except Exception as error:
            self.logger.error(error)
            return False

    async def close_pool(self) -> bool:
        try:
            is_closed = await self.connector.close_pool()
            self.logger.info(f'`ORM.connector: {self.connector.__class__.__name__}` pool closed')
            return is_closed
        except Exception as error:
            self.logger.error(f'{error}')
            return False

    def delete(self, *args, **kwargs) -> 'Delete':
        return Delete(*args, **kwargs)

    def select(self, *args, **kwargs) -> 'Select':
        return Select(*args, **kwargs)

    def insert(self, *args, **kwargs) -> Insert:
        return Insert(*args, **kwargs)

    def update(self, *args, **kwargs) -> Update:
        return Update(*args, **kwargs)
