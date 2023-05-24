from src.apidevtools.security import encryptor
import asyncio
from time import perf_counter

import enc_sync
import enc_async


async def async_benchmark():
    t0 = perf_counter()

    raw, master, auth = 'raw', 'master', 'myauth'

    encrypted, key = await enc_async.encrypt(raw)
    assert await enc_async.decrypt(encrypted, key, evaluate=True) == raw

    encrypted, key = await enc_async.encrypt(raw, authdata=auth.encode())
    assert await enc_async.decrypt(encrypted, key, authdata=auth.encode(), evaluate=True) == raw

    # encrypted, key = encryptor.encrypt(raw, authdata=auth.encode())
    # assert encryptor.decrypt(encrypted, key, authdata='nonauth', evaluate=True) != raw

    encrypted, key = await enc_async.encrypt(raw, masterkey=master)
    assert await enc_async.decrypt(encrypted, key, masterkey=master, evaluate=True) == raw

    # encrypted, key = encryptor.encrypt(raw, masterkey=master)
    # assert encryptor.decrypt(encrypted, key, masterkey='nonmaster', evaluate=True) != raw

    encrypted, key = await enc_async.encrypt(raw, masterkey=master, authdata=auth.encode())
    assert await enc_async.decrypt(encrypted, key, masterkey=master, authdata=auth.encode(), evaluate=True) == raw

    t1 = perf_counter()
    print('took: %2.4f sec' % (t1 - t0))


def sync_benchmark():
    t0 = perf_counter()

    raw, master, auth = 'raw', 'master', 'myauth'

    encrypted, key = enc_sync.encrypt(raw)
    assert enc_sync.decrypt(encrypted, key, evaluate=True) == raw

    encrypted, key = enc_sync.encrypt(raw, authdata=auth.encode())
    assert enc_sync.decrypt(encrypted, key, authdata=auth.encode(), evaluate=True) == raw

    # encrypted, key = encryptor.encrypt(raw, authdata=auth.encode())
    # assert encryptor.decrypt(encrypted, key, authdata='nonauth', evaluate=True) != raw

    encrypted, key = enc_sync.encrypt(raw, masterkey=master)
    assert enc_sync.decrypt(encrypted, key, masterkey=master, evaluate=True) == raw

    # encrypted, key = encryptor.encrypt(raw, masterkey=master)
    # assert encryptor.decrypt(encrypted, key, masterkey='nonmaster', evaluate=True) != raw

    encrypted, key = enc_sync.encrypt(raw, masterkey=master, authdata=auth.encode())
    assert enc_sync.decrypt(encrypted, key, masterkey=master, authdata=auth.encode(), evaluate=True) == raw

    t1 = perf_counter()
    print('took: %2.4f sec' % (t1 - t0))


def apidevtools_benchmark():
    t0 = perf_counter()

    raw, master, auth = 'raw', 'master', 'myauth'

    encrypted, key = encryptor.encrypt(raw)
    assert encryptor.decrypt(encrypted, key, evaluate=True) == raw

    encrypted, key = encryptor.encrypt(raw, authdata=auth.encode())
    assert encryptor.decrypt(encrypted, key, authdata=auth.encode(), evaluate=True) == raw

    # encrypted, key = encryptor.encrypt(raw, authdata=auth.encode())
    # assert encryptor.decrypt(encrypted, key, authdata='nonauth', evaluate=True) != raw

    encrypted, key = encryptor.encrypt(raw, masterkey=master)
    assert encryptor.decrypt(encrypted, key, masterkey=master, evaluate=True) == raw

    # encrypted, key = encryptor.encrypt(raw, masterkey=master)
    # assert encryptor.decrypt(encrypted, key, masterkey='nonmaster', evaluate=True) != raw

    encrypted, key = encryptor.encrypt(raw, masterkey=master, authdata=auth.encode())
    assert encryptor.decrypt(encrypted, key, masterkey=master, authdata=auth.encode(), evaluate=True) == raw

    t1 = perf_counter()
    print('took: %2.4f sec' % (t1 - t0))


asyncio.get_event_loop().run_until_complete(async_benchmark())
sync_benchmark()
apidevtools_benchmark()
