import asyncio

from src.apidevtools.orm import ORM, connector


orm = ORM(
    connector=connector.PostgreSQL(
        database='database', user='postgres', password='password', host='localhost', port=5432
    )
)


async def amain():
    await orm.create_pool()

    await orm.select('column1', 'column2').fr0m('tablename').where(column3=3).order(column1='asc', column2='desc').limit(5).offset(3).all()
    print(orm._query)
    orm.update('tablename').set(column1='value1', column2='value2').where(column3=3)
    print(orm._query)
    orm.insert().into('table').values(column1='value1', column2='value2').returning(type=dict)
    print(orm._query)
    orm.insert().into('table').values('value1', 'value2')
    print(orm._query)
    orm.insert('instance')
    print(orm._query)
    orm.delete().fr0m('table').where(column1='value1')
    print(orm._query)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(amain())
