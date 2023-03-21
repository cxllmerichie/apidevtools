import asyncio as _asyncio
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
        self.user: str | None = user
        self.password: str | None = password

        self.logger: Logger = logger
        self.pool: _aioredis.Redis | None = None

    async def create_pool(self) -> bool:
        try:
            self.pool = _aioredis.Redis(
                host=self.host, port=self.port, username=self.user, password=self.password
            )
            return True
        except Exception as error:
            self.logger.error(error)
            return False

    async def close_pool(self) -> bool:
        try:
            await self.pool.close()
            return True
        except Exception as error:
            self.logger.error(error)
            return False

    def __getitem__(self, key) -> Any:
        try:
            async def evaluate():
                return _ast.literal_eval((await self.pool.get(key)).decode())
            return evaluate()
        except Exception as error:
            self.logger.error(error)
            return _asyncio.get_event_loop().run_in_executor(None, lambda: None)

    async def set(self, key: Any, value: Any) -> bool:
        try:
            return await self.pool.set(key, value)
        except Exception as error:
            self.logger.error(error)
            return False

    async def get(self, key: Any) -> bytes | None:
        try:
            return await self.pool.get(key)
        except Exception as error:
            self.logger.error(error)
            return None
