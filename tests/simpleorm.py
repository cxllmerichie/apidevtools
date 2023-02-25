from src.apidevtools.simpleorm import Schema, Relation, PostgreSQL


tables: str = '''
CREATE TABLE IF NOT EXISTS "user" (
    "id" SERIAL PRIMARY KEY,
    
    "email" TEXT NOT NULL UNIQUE,
    "password" TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS "category" (
    "id" SERIAL PRIMARY KEY,
    
    "title" TEXT NOT NULL UNIQUE,
    "description" TEXT NOT NULL,
    
    "user_id" INT NOT NULL,
    CONSTRAINT fk_user FOREIGN KEY("user_id") REFERENCES "user" ("id")
);

CREATE TABLE IF NOT EXISTS "item" (
    "id" SERIAL PRIMARY KEY,
    
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
            Relation('item', dict(category_id=id), User, 'items', Item, ['*'])
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
            Relation('category', dict(user_id=id), User, 'categories', Category, ['*'])
        ]


DB_NAME = "web_telegram_backup"
DB_USER = "postgres"
DB_PASS = "0FD1Vg44au{U@0<fn@=M"
DB_HOST = "localhost"
DB_PORT = 5432

db: PostgreSQL = PostgreSQL(database=DB_NAME, host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASS)


async def startup():
    assert await db.create_pool()
    await db.execute(tables)


async def shutdown():
    assert await db.close_pool()


async def amain():
    await startup()

    instance = UserCreate(email='string', password='string')
    db_user = await db.insert(instance, User)

    db_user.email = 's'
    db_user = await db.update(db_user, dict(id=db_user.id), User)

    await shutdown()


if __name__ == '__main__':
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(amain())
