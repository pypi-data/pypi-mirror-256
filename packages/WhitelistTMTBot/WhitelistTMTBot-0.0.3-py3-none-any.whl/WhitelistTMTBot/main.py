from .dataclass import RequestBodyClass
from .dbase import AsyncDatabase
from .server import AsyncHTTPClient

DB_FILE: str = "whitelist.db"
URL: str = "https://events.tmtsocket.com/event/bot-activated/"
HEADERS: dict = {"Content-Type": "application/json"}


async def check_conversion(user_id: str) -> bool:
    db = AsyncDatabase(DB_FILE)
    await db.connect()
    res = await db.check_user_in_whitelist(user_id)
    await db.close()
    return res


async def register_conversion(
    user_id: str, uuid: str, bot: str, request_body: RequestBodyClass
) -> bool:
    http_client = AsyncHTTPClient()
    db = AsyncDatabase(DB_FILE)
    await db.connect()
    response = await http_client.post(URL, request_body.to_dict(), HEADERS)
    await http_client.close()

    if response.status == 200:
        await db.add_to_whitelist(
            user_id=user_id,
            uuid=uuid,
            bot=bot,
        )
        await db.close()
        return True
    return False
