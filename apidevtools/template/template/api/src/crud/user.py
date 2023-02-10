from apidevtools import Hasher, Avatar

from .. import schemas
from ..const import db
from .item import get_items, delete_item


async def create_user(user: schemas.UserCreate) -> schemas.User:
    user.password = Hasher.hash(password=user.password)
    if not user.avatar_url:
        user.avatar_url = await Avatar.default().url()
    db_user = await db.insert(user, schemas.User)
    return db_user


async def get_user(user_id: int = None, email: str = None, schema: type = schemas.User) -> schemas.User | None:
    field, value = ('email', email) if email else ('id', user_id)
    query, args = f'SELECT * FROM "user" WHERE "{field}" = $1;', (value, )
    db_user = (await db.select(query, args, schema)).first()
    return db_user


async def update_user(user_id: int, user: schemas.UserUpdate) -> schemas.User:
    db_user = await get_user(user_id=user_id, schema=schemas.User)
    user.avatar_url = db_user.avatar_url if not user.avatar_url else user.avatar_url
    db_user = await db.update(user, dict(id=user_id), schemas.User)
    return db_user


async def delete_user(user_id: int) -> None:
    db_items = await get_items(user_id=user_id)
    for db_item in db_items:
        await delete_item(item_id=db_item.id)
    query, args = f'DELETE FROM "user" WHERE "id" = $1;', (user_id, )
    await db.execute(query, args)
