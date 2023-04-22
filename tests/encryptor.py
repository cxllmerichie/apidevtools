from src.apidevtools.security import encryptor, hasher


raw = 'raw'
encrypted, key = encryptor.encrypt(raw)
assert encryptor.decrypt(encrypted, key, convert=True) == raw


unhashed = 'unhashed'
hashed = hasher.hash(unhashed)
assert hasher.cmp(hashed, unhashed)
