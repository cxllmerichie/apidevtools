import asyncio
from loguru import logger

from src.apidevtools.simpleorm.connectors.mysql import MySQL
from src.apidevtools.simpleorm import ORM

from tests.orm.data import amain


tables: str = '''
CREATE TABLE IF NOT EXISTS simpleorm_user (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,

    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    
    CONSTRAINT unique_user UNIQUE (email)
);

CREATE TABLE IF NOT EXISTS simpleorm_category (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,

    title VARCHAR(255) NOT NULL,
    description VARCHAR(255) NOT NULL,

    user_id INT NOT NULL,
    CONSTRAINT fk_user FOREIGN KEY(user_id) REFERENCES simpleorm_user (id),
    CONSTRAINT unique_category UNIQUE (title)
);

CREATE TABLE IF NOT EXISTS simpleorm_item (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,

    title VARCHAR(255) NOT NULL,
    description VARCHAR(255) NOT NULL,

    category_id INT NOT NULL,
    CONSTRAINT fk_category FOREIGN KEY(category_id) REFERENCES simpleorm_category (id)
);
'''


if __name__ == '__main__':
    DB_NAME = 'mysql'
    DB_USER = 'user'
    DB_PASS = 'password'
    DB_HOST = 'localhost'
    DB_PORT = 3306

    db: ORM = ORM(
        connector=MySQL(database=DB_NAME, host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASS),
        logger=logger
    )

    loop = asyncio.get_event_loop()
    loop.run_until_complete(amain(db, tables))
