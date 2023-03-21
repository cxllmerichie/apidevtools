import asyncio
from loguru import logger

from src.apidevtools.simpleorm.connectors.sqlite import SQLite
from src.apidevtools.simpleorm import Schema, Relation, ORM


tables: str = '''
CREATE TABLE IF NOT EXISTS "user" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,

    "email" TEXT NOT NULL UNIQUE,
    "password" TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS "category" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,

    "title" TEXT NOT NULL UNIQUE,
    "description" TEXT NOT NULL,

    "user_id" INT NOT NULL,
    CONSTRAINT fk_user FOREIGN KEY("user_id") REFERENCES "user" ("id")
);

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


DB_NAME = 'sqlite.sqlite'

db: ORM = ORM(
    connector=SQLite(database=DB_NAME),
    logger=logger
)


async def startup():
    assert await db.create_pool()
    print(await db.execute(tables))


async def shutdown():
    assert await db.close_pool()


async def amain():
    await startup()

    for i in range(10):
        instance = UserCreate(email=f'string{i}', password='string')
        db_user = await db.insert(instance, User)
        print(db_user)

    db_users = await db.select('SELECT * FROM "user";')
    print(db_users.order_by(['id', 'email']).all())
    print(db_users.first())
    for db_user in db_users:
        print(db_user)

    await shutdown()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(amain())
