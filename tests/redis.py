import asyncio

from src.apidevtools.simpleorm.redis import Redis


async def amain():
    db = Redis(database=0, host='localhost', port=6379, password="LAIOAyNd9`H4v{FrWs2c8p2e=y552v#3L6[4U]b1<4u@?#]C&2")
    await db.create_pool()

    print(await db.set('key', 32))
    print(await db.get('key'))
    print(await db.delete('key'))

    await db.close_pool()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(amain())
