from . import AsyncDatabase, AsyncHTTPClient, RequestBodyClass

DB_FILE: str = "whitelist.db"
URL: str = "https://events.tmtsocket.com/event/bot-activated/"
HEADERS: dict = {"Content-Type": "application/json"}


class Whitelist:
    def __init__(self, db_file: str = DB_FILE) -> None:
        self.db_file = db_file
        self.http_client: AsyncHTTPClient = AsyncHTTPClient()
        self.database: AsyncDatabase = AsyncDatabase(self.db_file)
        self.build()

    async def build(self):
        await self.database.connect()
        await self.database.create_whitelist_table()

    async def check_conversion(self, user_id: str) -> bool:
        res = await self.database.check_user_in_whitelist(user_id)
        await self.database.close()
        return res

    async def register_conversion(
        self, user_id: str, uuid: str, bot: str, request_body: RequestBodyClass
    ) -> bool:
        response = await self.http_client.post(URL, request_body.to_dict(), HEADERS)
        await self.http_client.close()

        if response.status == 200:
            await self.database.add_to_whitelist(
                user_id=user_id,
                uuid=uuid,
                bot=bot,
            )
            await self.database.close()
            return True
        return False
