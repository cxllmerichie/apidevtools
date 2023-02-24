from apidevtools.simpleorm import Schema, Relation


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

    items: list[Item]

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

    categories: list[Category]

    def relations(self) -> list[Relation]:
        return [
            Relation('category', dict(user_id=id), User, 'categories', Category, ['*'])
        ]
