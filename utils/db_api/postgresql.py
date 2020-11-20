import asyncio

import asyncpg

from data import config


class Database:
    def __init__(self, loop: asyncio.AbstractEventLoop):
        self.pool: asyncio.pool.Pool = loop.run_until_complete(
            asyncpg.create_pool(
                user=config.PGUSER,
                password=config.PGPASSWORD,
                host=config.ip
            )
        )

    async def create_table_news(self):
        sql = """
        CREATE TABLE IF NOT EXISTS News (
        id SERIAL PRIMARY KEY,
        user_id int NOT NULL,
        content TEXT,
        photo_id TEXT,
        caption TEXT,
        username VARCHAR NOT NULL
        )
        """
        await self.pool.execute(sql)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f'{item} = ${num}' for num, item in enumerate(parameters, start=1)
        ])
        return sql, tuple(parameters.values())

    async def add_news(self, user_id: int, content: str, photo_id: str, caption: str, username: str):
        sql = "INSERT INTO News(user_id, content, photo_id, caption, username) VALUES($1, $2, $3, $4, $5)"
        # parameters = (user_id, content, photo_id, caption, username)
        await self.pool.execute(sql, user_id, content, photo_id, caption, username)

    async def select_all_news(self):
        sql = "SELECT * FROM News"
        return await self.pool.fetch(sql)

    async def select_one_news(self, **kwargs):
        sql = "SELECT * FROM News WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return await self.pool.fetchrow(sql, *parameters)

    async def delete_news(self, **kwargs):
        sql = 'DELETE FROM News WHERE '
        sql, parameters = self.format_args(sql, kwargs)
        await self.pool.execute(sql, *parameters)

# db = Database(loop=asyncio.get_event_loop())
