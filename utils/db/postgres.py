from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config


class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME,
        )

    async def execute(
            self,
            command,
            *args,
            fetch: bool = False,
            fetchval: bool = False,
            fetchrow: bool = False,
            execute: bool = False,
    ):

        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
        id SERIAL PRIMARY KEY,
        full_name TEXT NULL,
        username TEXT NULL,
        telegram_id BIGINT NOT NULL UNIQUE,
        phone TEXT NULL
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join(
            [f"{item} = ${num}" for num, item in enumerate(parameters.keys(), start=1)]
        )
        return sql, tuple(parameters.values())

    async def add_user(self, full_name, username, telegram_id):
        sql = "INSERT INTO users (full_name, username, telegram_id) VALUES($1, $2, $3) returning *"
        return await self.execute(sql, full_name, username, telegram_id, fetchrow=True)

    async def select_all_users(self):
        sql = "SELECT * FROM Users"
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM Users"
        return await self.execute(sql, fetchval=True)

    async def update_user_username(self, username, telegram_id):
        sql = "UPDATE Users SET username=$1 WHERE telegram_id=$2"
        return await self.execute(sql, username, telegram_id, execute=True)

    async def delete_users(self):
        await self.execute("DELETE FROM Users WHERE TRUE", execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE Users", execute=True)

# ==================== DO'KONLAR JADVALI ====================
    async def create_table_shops(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Shops (
        id SERIAL PRIMARY KEY,
        name TEXT NULL,
        region TEXT NULL,
        city TEXT NULL,
        address TEXT NULL,
        longitude FLOAT NULL,
        latitude FLOAT NULL,
        landmark TEXT NULL,
        phone TEXT NULL,
        image TEXT NULL
        );
        """
        await self.execute(sql, execute=True)

    async def add_shop(self, name, region, city, address, longitude, latitude, landmark, phone, image):
        sql = ("INSERT INTO Shops (name, region, city, address, longitude, latitude, landmark, phone, image) "
               "VALUES($1, $2, $3, $4, $5, $6, $7, $8, $9) returning id")
        return await self.execute(sql, name, region, city, address, longitude, latitude,
                                  landmark, phone, image, fetchrow=True)

    async def select_all_shops(self):
        sql = "SELECT id, name FROM Shops"
        return await self.execute(sql, fetch=True)

    async def select_shop_by_id(self, id_):
        sql = f"SELECT * FROM Shops WHERE id='{id_}'"
        return await self.execute(sql, fetchrow=True)

    async def drop_shops(self):
        await self.execute("DROP TABLE Shops", execute=True)

# ==================== KITOBLAR JADVALI ====================
    async def create_table_books(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Books (
        id SERIAL PRIMARY KEY,
        shop_id INT NULL,
        book TEXT NULL,        
        price FLOAT NULL,        
        FOREIGN KEY (shop_id) REFERENCES Shops(id)        
        );
        """
        await self.execute(sql, execute=True)

    async def add_books(self, shop_id, book, price, image):
        sql = "INSERT INTO Books (shop_id, book, price, image) VALUES($1, $2, $3, $4) returning id"
        return await self.execute(sql, shop_id, book, price, image, fetchrow=True)

    async def select_book(self, book):
        sql = "SELECT * FROM Books WHERE book=$1"
        return await self.execute(sql, book, fetch=True)

    async def select_books(self):
        sql = "SELECT * FROM Books ORDER BY book"
        return await self.execute(sql, fetch=True)

    async def drop_books(self):
        await self.execute("DROP TABLE Books", execute=True)
