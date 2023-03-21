import asyncio
from loguru import logger

from src.apidevtools.simpleorm.connectors.sqlite import SQLite
from src.apidevtools.simpleorm import ORM

from tests.orm.data import amain


tables: str = '''
CREATE TABLE IF NOT EXISTS "simpleorm_user" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,

    "email" TEXT NOT NULL UNIQUE,
    "password" TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS "simpleorm_category" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,

    "title" TEXT NOT NULL UNIQUE,
    "description" TEXT NOT NULL,

    "user_id" INT NOT NULL,
    CONSTRAINT fk_user FOREIGN KEY("user_id") REFERENCES "simpleorm_user" ("id")
);

CREATE TABLE IF NOT EXISTS "simpleorm_item" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,

    "title" TEXT NOT NULL,
    "description" TEXT NOT NULL,

    "category_id" INT NOT NULL,
    CONSTRAINT fk_category FOREIGN KEY("category_id") REFERENCES "simpleorm_category" ("id")
);
'''


if __name__ == '__main__':
    DB_NAME = 'simpleorm_sqlite.sqlite'

    db: ORM = ORM(
        # connector=SQLite(database=DB_NAME),
        connector=SQLite(),
        logger=logger
    )

    loop = asyncio.get_event_loop()
    loop.run_until_complete(amain(db, tables))
