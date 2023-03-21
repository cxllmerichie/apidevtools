import aioredis as _aioredis
import loguru
from loguru._logger import Logger
import ast as _ast
from typing import Any


class Redis:
    def __init__(self, host: str, port: int | str, user: str | None = None, password: str | None = None,
                 logger: Logger = loguru.logger):
        self.host: str = host
        self.port: str | int = port
        self.user: str = user
        self.password: str | None = password

        self.logger: Logger = logger

        self.pool: _aioredis.Redis | None = None

    async def create_pool(self) -> bool:
        try:
            self.pool = _aioredis.Redis(
                host=self.host, port=self.port, username=self.user, password=self.password
            )
        except Exception as error:
            self.logger.error(error)
            return False
        return True

    async def close_pool(self) -> bool:
        try:
            await self.pool.close()
        except Exception as error:
            self.logger.error(error)
            return False
        return True

    def __getitem__(self, key):
        async def convert():
            value: bytes = await self.pool.get(key)
            return _ast.literal_eval(value.decode())
        return convert()

    async def set(self, key: Any, value: Any):
        return await self.pool.set(key, value)

    async def get(self, key: Any):
        return await self.pool.get(key)
