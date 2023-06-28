import asyncio

from src.apidevtools.simpleorm.connectors.postgresql import PostgreSQL
from src.apidevtools.simpleorm import ORM
from src.apidevtools.logman import LoggerManager

from tests.orm.data import amain


tables: str = '''
CREATE TABLE IF NOT EXISTS "simpleorm_user" (
    "id" SERIAL PRIMARY KEY,

    "email" TEXT NOT NULL UNIQUE,
    "password" TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS "simpleorm_category" (
    "id" SERIAL PRIMARY KEY,

    "title" TEXT NOT NULL UNIQUE,
    "description" TEXT NOT NULL,

    "user_id" INT NOT NULL,
    CONSTRAINT "fk_user" FOREIGN KEY("user_id") REFERENCES "simpleorm_user" ("id")
);

CREATE TABLE IF NOT EXISTS "simpleorm_item" (
    "id" SERIAL PRIMARY KEY,

    "title" TEXT NOT NULL,
    "description" TEXT NOT NULL,

    "category_id" INT NOT NULL,
    CONSTRAINT "fk_category" FOREIGN KEY("category_id") REFERENCES "simpleorm_category" ("id")
);
'''


if __name__ == '__main__':
    DB_NAME = "simpleorm_postgresql"
    DB_USER = "postgres"
    DB_PASS = "0FD1Vg44au{U@0<fn@=M"
    DB_HOST = "localhost"
    DB_PORT = 5432

    db: ORM = ORM(
        connector=PostgreSQL(database=DB_NAME, host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASS),
        logger=LoggerManager.logger()
    )

    loop = asyncio.get_event_loop()
    loop.run_until_complete(amain(db, tables))
