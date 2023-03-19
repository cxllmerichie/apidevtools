from src.apidevtools.security import encryptor, hasher


key = '1234123412341234'
raw = 'toencrypt'
encrypted, iv = encryptor.encrypt(raw, key)
assert encryptor.decrypt(encrypted, key, iv) == raw

unhashed = 'sometgingtohash'
hashed = hasher.hash(unhashed)
assert hasher.cmp(hashed, unhashed)
