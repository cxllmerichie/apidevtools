import asyncio

import aiosqlite
from loguru._logger import Logger
from typing import Any, MutableMapping
import loguru

from src.apidevtools.simpleorm.types import Records, Relation, Schema
from src.apidevtools.simpleorm.connector._base import SQLConnector


class SQLite(SQLConnector):
    def __init__(self, database: str,
                 logger: Logger = loguru.logger):
        self.database: str = database if database.endswith('.sqlite') else f'{database}.sqlite'

        self.logger: Logger = logger

        self.pool: aiosqlite.Connection | None = None

    async def create_pool(self) -> bool:
        try:
            self.pool = await aiosqlite.connect(database=self.database)
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

    async def execute(self, query: str, args: tuple[Any, ...] = ()) -> Any:
        try:
            if len(args):
                cursor: aiosqlite.Cursor = await self.pool.execute(query, args)
            else:
                cursor: aiosqlite.Cursor = await self.pool.executescript(query)
            await self.pool.commit()
            return cursor.description
        except Exception as error:
            self.logger.error(error)

    async def columns(self, tablename: str) -> list[str]:
        try:
            cursor: aiosqlite.Cursor = await self.pool.execute(f'SELECT * FROM {tablename}')
            await self.pool.commit()
            return list(map(lambda x: x[0], cursor.description))
        except Exception as error:
            self.logger.error(error)
        return []

    async def fetchall(self, query: str, args: tuple[Any, ...] = ()) -> list[MutableMapping]:
        try:
            cursor: aiosqlite.Cursor = await self.pool.execute(query, args)
            result = [{cursor.description[i][0]: value for i, value in enumerate(row)} for row in await cursor.fetchall()]
            await self.pool.commit()
            return result
        except Exception as error:
            self.logger.error(error)
        return []

    async def constructor__select_relation(
            self, relation: Relation
    ) -> tuple[str, tuple[Any, ...]]:
        columns, values = ', '.join(relation.columns), tuple(relation.where.values())
        conditions = ' AND '.join([f'{key} = ?' for key in relation.where.keys()])
        return f'SELECT {columns} FROM "{relation.tablename}" WHERE {conditions};', values

    async def constructor__select_instance(
            self,
            instance: dict, tablename: str
    ) -> tuple[str, tuple[Any, ...]]:
        conditions = ' AND '.join([f'{key} = ?' for key in instance.keys()])
        return f'SELECT * FROM "{tablename}" WHERE {conditions};', tuple(instance.values())

    async def constructor__insert_instance(
            self,
            instance: dict, tablename: str
    ) -> tuple[str, tuple[Any, ...]]:
        placeholders = ', '.join(['?' for _ in range(len(instance.keys()))])
        columns, values = str(tuple(instance.keys())).replace("'", '"'), instance.values()
        return f'INSERT INTO "{tablename}" {columns} VALUES ({placeholders}) RETURNING *;', tuple(values)

    async def constructor__update_instance(
            self,
            instance: dict, tablename: str, where: dict[str, Any]
    ) -> tuple[str, tuple[Any, ...]]:
        values = ', '.join([f'{key} = ?' for key in instance.keys()])
        conditions = ' AND '.join([f'"{key}" = \'{value}\'' for key, value in where.items()])
        return f'UPDATE "{tablename}" SET {values} WHERE {conditions} RETURNING *;', tuple(instance.values())

    async def constructor__delete_instance(
            self,
            instance: dict, tablename: str
    ) -> tuple[str, tuple[Any, ...]]:
        conditions = ' AND '.join([f'{key} = ?' for key in instance.keys()])
        return f'DELETE FROM "{tablename}" WHERE {conditions} RETURNING *;', tuple(instance.values())


user: str = '''
CREATE TABLE IF NOT EXISTS "user" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,

    "email" TEXT NOT NULL UNIQUE,
    "password" TEXT NOT NULL
);'''

category = '''
CREATE TABLE IF NOT EXISTS "category" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,

    "title" TEXT NOT NULL UNIQUE,
    "description" TEXT NOT NULL,

    "user_id" INT NOT NULL,
    CONSTRAINT fk_user FOREIGN KEY("user_id") REFERENCES "user" ("id")
);'''

item = '''
CREATE TABLE IF NOT EXISTS "item" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,

    "title" TEXT NOT NULL,
    "description" TEXT NOT NULL,

    "category_id" INT NOT NULL,
    CONSTRAINT fk_category FOREIGN KEY("category_id") REFERENCES "category" ("id")
);
'''


class ItemBase(Schema):
    __tablename__ = 'category'

    title: str
    description: str


class ItemCreate(ItemBase):
    ...


class ItemCreateCrud(ItemBase):
    category_id: int


class Item(ItemCreateCrud):
    id: int


class CategoryBase(Schema):
    __tablename__ = 'category'

    title: str
    description: str


class CategoryCreate(CategoryBase):
    ...


class Category(CategoryBase):
    id: int

    items: list[Item] = []

    def relations(self) -> list[Relation]:
        return [
            Relation('item', dict(category_id=self.id), User, 'items', Item, ['*'])
        ]


class UserBase(Schema):
    __tablename__ = 'user'

    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    categories: list[Category] = []

    def relations(self) -> list[Relation]:
        return [
            Relation('category', dict(user_id=self.id), User, 'categories', Category, ['*'])
        ]

from loguru import logger

from src.apidevtools.simpleorm import Schema, Relation, ORM


DB_NAME = 'sqlite.sqlite'

db: ORM = ORM(
    connector=SQLite(database=DB_NAME),
    logger=logger
)


async def startup():
    assert await db.create_pool()
    print(await db.execute(user))
    await db.execute(category)
    await db.execute(item)


async def shutdown():
    assert await db.close_pool()


async def amain():
    await startup()

    for i in range(10):
        instance = UserCreate(email=f'string{i}', password='string')
        db_user = await db.insert(instance, User)
        print(db_user)

    async for i in await db.select('SELECT * FROM "user";'):
        print(i)

    await shutdown()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(amain())
