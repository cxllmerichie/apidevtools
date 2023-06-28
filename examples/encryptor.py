from src.apidevtools.security import encryptor
from time import perf_counter


def benchmark():
    t0 = perf_counter()

    raw, master, auth = 'raw', 'master', 'myauth'

    # took: 0.0001 sec
    encrypted, key = encryptor.encrypt(raw)
    assert encryptor.decrypt(encrypted, key, evaluate=True) == raw

    # took: 0.0001 sec
    encrypted, key = encryptor.encrypt(raw, authdata=auth.encode())
    assert encryptor.decrypt(encrypted, key, authdata=auth.encode(), evaluate=True) == raw

    # took: 0.15 sec
    encrypted, key = encryptor.encrypt(raw, masterkey=master)
    assert encryptor.decrypt(encrypted, key, masterkey=master, evaluate=True) == raw

    # took: 0.15 sec
    encrypted, key = encryptor.encrypt(raw, masterkey=master, authdata=auth.encode())
    assert encryptor.decrypt(encrypted, key, masterkey=master, authdata=auth.encode(), evaluate=True) == raw

    # took: 0.004 sec
    encrypted, key = encryptor.encrypt(raw, compressed=True)
    assert encryptor.decrypt(encrypted, key, evaluate=True, compressed=True) == raw

    # took: 0.15 sec
    encrypted, key = encryptor.encrypt(raw, masterkey=master, authdata=auth.encode(), compressed=True)
    assert encryptor.decrypt(encrypted, key, masterkey=master, authdata=auth.encode(), evaluate=True, compressed=True) == raw

    t1 = perf_counter()
    print('took: %2.4f sec' % (t1 - t0))


benchmark()
