import asyncio

from src.apidevtools import orm


db = orm.postgresql.PostgreSQL(
    database='temp', user='postgres', password='BAb231wAtCp4hWAt66', host='158.220.110.33', port=5432
)


async def amain():
    await db.create_pool()

    await db.execute('''
        CREATE TABLE IF NOT EXISTS "tablename" (
            "column1" TEXT PRIMARY KEY,
            "column2" TEXT
        );
    ''')

    for i in range(10):
        rv = await db.insert().into('tablename').values(f'column1_{i}', f'column2_{i}').one()
        # print(rv)

    with db.select('*').fr0m('tablename').returning(type=dict) as rows:
        async for row in rows:
            # print(row)
            ...

    rows = await db.select('*').fr0m('tablename').all()
    print(row)

    await db.delete().fr0m('tablename').exec()

    # await db.select('column1', 'column2').fr0m('tablename').where(column3=3).order(column1='asc', column2='desc').limit(5).offset(3).all()
    # print(db._query)
    # db.update('tablename').set(column1='value1', column2='value2').where(column3=3)
    # print(db._query)
    # db.insert().into('table').values(column1='value1', column2='value2').returning(type=dict)
    # print(db._query)
    # db.insert().into('table').values('value1', 'value2')
    # print(db._query)
    # db.insert('instance')
    # print(db._query)
    # db.delete().fr0m('table').where(column1='value1')
    # print(db._query)

    await db.close_pool()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(amain())
