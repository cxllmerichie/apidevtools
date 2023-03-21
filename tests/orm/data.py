from pydantic import Field

from src.apidevtools.simpleorm import Schema, Relation


class ItemBase(Schema):
    __tablename__ = 'item'

    title: str
    description: str


class ItemCreate(ItemBase):
    ...


class ItemCreateCrud(ItemCreate):
    category_id: int


class Item(ItemCreateCrud):
    id: int

    category_id: int


class CategoryBase(Schema):
    __tablename__ = 'category'

    title: str
    description: str | None = None


class CategoryCreate(CategoryBase):
    ...


class CategoryCreateCrud(CategoryCreate):
    user_id: int


class Category(CategoryBase):
    id: int

    items: list[Item] = []
    user_id: int

    def relations(self) -> list[Relation]:
        return [
            Relation('item', dict(category_id=self.id), Category, 'items', Item, ['*'])
        ]


class UserBase(Schema):
    __tablename__ = 'user'

    email: str = Field()


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    categories: list[Category] = []

    def relations(self) -> list[Relation]:
        return [
            Relation('category', dict(user_id=self.id), User, 'categories', Category, ['*'])
        ]


async def startup(db, tables):
    assert await db.create_pool()
    await db.execute(tables)


async def shutdown(db):
    assert await db.close_pool()


async def amain(db, tables):
    await startup(db, tables)

    instance = UserCreate(email=f'string', password='string')
    db_user = await db.insert(instance, User)

    category = CategoryCreateCrud(title='title', description='description', user_id=db_user.id)
    db_category = await db.insert(category, Category)

    item = ItemCreateCrud(title='title', description='description', category_id=db_category.id)
    db_item = await db.insert(item, Item)

    db_user = (await db.select('SELECT * FROM "user";', schema_t=User, depth=2)).first()

    db_user = (await db.delete(db_user, User, depth=2)).first()
    print(db_user)

    await shutdown(db)
