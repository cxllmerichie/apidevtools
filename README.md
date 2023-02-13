## Overview
## Documentation
## Installation
```
pip install apidevtools
```
### Package dependencies
```
pip install asyncpg pydantic loguru telegraph pillow numpy argon2-cffi pycryptodome telegraph httpx aiohttp python-dateutil
```
speedups
```
pip install aiodns ujson cchardet uvloop
```
### Per module dependencies
- simpleorm
    ```
    pip install asyncpg pydantic loguru
    ```
- avatar
    ```
    pip install telegraph pillow numpy
    ```
- security
    - hasher
        ```
        pip install argon2-cffi
        ```
    - encryptor
        ```
        pip install pycryptodome
        ```
- telegraph
    ```
    pip install telegraph httpx aiohttp
    ```
    speedups:
    ```
    pip install aiodns cchardet  
    ```
- datetime
    ```
    pip install python-dateutil
    ```
# Further updates:
- import encapsulation (from outer_package import something as _something)

