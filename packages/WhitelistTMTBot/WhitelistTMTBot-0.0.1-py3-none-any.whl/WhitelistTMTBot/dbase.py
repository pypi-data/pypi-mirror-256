import logging

import aiosqlite

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AsyncDatabase:
    def __init__(self, db_file: str):
        self.db_file = db_file
        self.conn = None

    async def connect(self):
        self.conn = await aiosqlite.connect(self.db_file)
        logger.info("Database connection established.")

    async def close(self):
        await self.conn.close()
        logger.info("Database connection closed.")

    async def execute_query(self, query: str, params=()):
        async with self.conn.execute(query, params) as cursor:
            await self.conn.commit()
        logger.info("Query executed.")

    async def execute_read_query(self, query: str, params=()):
        cursor = await self.conn.execute(query, params)
        rows = await cursor.fetchall()
        return rows

    async def create_whitelist_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS whitelist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            uuid TEXT NOT NULL,
            bot TEXT NOT NULL
        );
        """
        await self.execute_query(query)
        logger.info("Table 'whitelist' created.")

    async def check_user_in_whitelist(self, user_id: str) -> bool:
        query = "SELECT 1 FROM whitelist WHERE user_id = ? LIMIT 1;"
        result = await self.execute_read_query(query, (user_id,))
        return bool(result)

    async def add_to_whitelist(self, user_id: str, uuid: str, bot: str):
        query = "INSERT INTO whitelist (user_id, uuid, bot) VALUES (?, ?, ?);"
        await self.execute_query(query, (user_id, uuid, bot))
        logger.info(f"User {user_id} added to whitelist.")
