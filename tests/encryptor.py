from src.apidevtools.security import encryptor, hasher


raw = 'toencrypt'
encrypted, key = encryptor.encrypt(raw)
assert encryptor.decrypt(encrypted, key, convert=True) == raw


unhashed = 'sometgingtohash'
hashed = hasher.hash(unhashed)
assert hasher.cmp(hashed, unhashed)
