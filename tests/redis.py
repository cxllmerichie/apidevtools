import asyncio

from src.apidevtools.simpleorm.nosql import Redis


loop = asyncio.get_event_loop()


async def amain():
    db = Redis(host='localhost', port=6379, password="h1=Q3mU3&O92v'<otR-V")
    await db.create_pool()

    await db.set('key', 1)
    print(await db['key'])
    print(await db.get('key'))

    await db.close_pool()

if __name__ == '__main__':
    loop.run_until_complete(amain())
