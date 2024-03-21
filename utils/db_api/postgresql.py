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
            database=config.DB_NAME
        )

    async def execute(self, command, *args,
                    fetch: bool = False,
                    fetchval: bool = False,
                    fetchrow: bool = False,
                    execute: bool = False
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
            phone VARCHAR(20),
            full_name VARCHAR(255),
            age INTEGER,
            username varchar(255),
            telegram_id BIGINT NOT NULL UNIQUE DEFAULT 123,
            first_step BOOLEAN DEFAULT FALSE,
            test_step BOOLEAN DEFAULT FALSE,
            result VARCHAR(255),
            filial VARCHAR(255),
            finish_step BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                        start=1)
        ])
        return sql, tuple(parameters.values())

    async def add_user(self, telegram_id):
        sql = "INSERT INTO users (telegram_id) VALUES ($1) returning *"
        return await self.execute(sql, telegram_id, fetchrow=True)
    
    async def add_default_user(self):
        sql = "INSERT INTO users (telegram_id) VALUES (1234567) returning *"
        return await self.execute(sql, fetchrow=True)

    async def update_user(self, phone, full_name, age, username, telegram_id):
        sql = "UPDATE users SET phone=$1, full_name=$2, age=$3, username=$4, first_step=True WHERE telegram_id=$5 returning *"
        return await self.execute(sql, phone, full_name, age, username, telegram_id, execute=True)

    async def select_all_telegram_ids(self, telegram_id):
        sql = "SELECT telegram_id FROM users WHERE telegram_id = $1"
        return await self.execute(sql, telegram_id, fetch=True)

    async def select_all_users(self):
        sql = "SELECT * FROM Users"
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)
    
    async def select_finished_user(self, telegram_id):
        sql = "SELECT id, phone, full_name, age, username, result, filial FROM Users WHERE telegram_id = $1"
        return await self.execute(sql, telegram_id, fetchrow=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM Users"
        return await self.execute(sql, fetchval=True)

    async def update_user_username(self, username, telegram_id):
        sql = "UPDATE Users SET username=$1 WHERE telegram_id=$2"
        return await self.execute(sql, username, telegram_id, execute=True)
    
    async def update_user_test_step(self, telegram_id):
        sql = "UPDATE Users SET test_step=True WHERE telegram_id=$1"
        return await self.execute(sql, telegram_id, execute=True)
    
    # async def update_user_interesting_step(self, telegram_id):
    #     sql = "UPDATE Users SET interesting_step=True WHERE telegram_id=$1"
    #     return await self.execute(sql, telegram_id, execute=True)
    
    async def update_user_finish_step(self, filial, telegram_id):
        sql = "UPDATE Users SET filial=$1, finish_step=True WHERE telegram_id=$2"
        return await self.execute(sql, filial, telegram_id, execute=True)
    
    async def update_user_result(self, result, telegram_id):
        sql = "UPDATE Users SET result=$1 WHERE telegram_id=$2"
        return await self.execute(sql, result, telegram_id, execute=True)

    async def delete_users(self):
        await self.execute("DELETE FROM Users WHERE TRUE", execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE IF EXISTS Users", execute=True)
        