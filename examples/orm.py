from dotenv import load_dotenv
import asyncio
import time
import os

from src.apidevtools.orm.mysql import MySQL
from src.apidevtools.orm.postgresql import PostgreSQL
from src.apidevtools.orm.sqlite import SQLite
from src.apidevtools.orm.types import Schema


assert load_dotenv('.env')


class Record(Schema):
    __tablename__ = 'tablename'

    column1: str
    column2: str


async def main(db):
    t0 = time.time_ns()
    assert await db.create_pool()

    await db.execute('''
        CREATE TABLE IF NOT EXISTS tablename (
            column1 text,
            column2 text
        );
    ''')
    for i in range(10):
        record = await db.insert().into('tablename').values(f'column1_{i}', f'column2_{i}').one(Record)
    async for record in db.records('SELECT * FROM tablename;'):
        ...
    async for record in db.select('*').fr0m('tablename').returning(type=Record):
        ...
    records = await db.fetchall(db.select('*').fr0m('tablename'))
    records = await db.select('*').fr0m('tablename').all(Record)
    record = await db.delete().fr0m('tablename').where(column1='column1_0').one(Record)
    await db.delete().fr0m('tablename').exec()

    assert await db.close_pool()
    t1 = time.time_ns()
    print((t1 - t0) / 1e+9)


if __name__ == '__main__':
    for db in [
        PostgreSQL(
            database=os.getenv('POSTGRES_DB'),
            user=os.getenv('POSTGRES_USER'), password=os.getenv('POSTGRES_PASS'),
            host=os.getenv('POSTGRES_HOST'), port=int(os.getenv('POSTGRES_PORT')),
        ),
        MySQL(
            database=os.getenv('MYSQL_DB'),
            user=os.getenv('MYSQL_USER'), password=os.getenv('MYSQL_PASS'),
            host=os.getenv('MYSQL_HOST'), port=int(os.getenv('MYSQL_PORT')),
        ),
        SQLite(
            database='sqlite.db'
        ),
        SQLite()
    ]:
        asyncio.new_event_loop().run_until_complete(main(db))
