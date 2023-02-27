## Overview
## Documentation
## Installation
```
pip install apidevtools
```
### Package dependencies
```
pip install asyncpg pydantic loguru pillow numpy argon2-cffi pycryptodome aiohttp
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
- security
    - hasher
        ```
        pip install argon2-cffi
        ```
    - encryptor
        ```
        pip install pycryptodome
        ```
- media
    - imgproc
        ```
        pip install pillow numpy
        ```
    - telegraph
        ```
        pip install aiohttp
        ```
- logman
    ```
    pip install loguru
    ```
