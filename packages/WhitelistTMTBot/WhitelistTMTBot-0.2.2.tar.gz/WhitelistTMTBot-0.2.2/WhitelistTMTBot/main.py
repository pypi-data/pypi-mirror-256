from .dataclass import RequestBodyClass
from .dbase import Database
from .server import HTTPClient

DB_FILE: str = "whitelist.db"
URL: str = "https://events.tmtsocket.com/event/bot-activated/"
HEADERS: dict = {"Content-Type": "application/json"}


class Whitelist:
    def __init__(self, db_file: str = DB_FILE) -> None:
        self.db_file = db_file
        self.http_client = None
        self.database = None

    def initialize(self):
        self.http_client = HTTPClient()
        self.database = Database(self.db_file)
        self.database.connect()
        self.database.create_whitelist_table()

    def check_conversion(self, user_id: str) -> bool:
        res = self.database.check_user_in_whitelist(user_id)
        self.database.close()
        return res

    def register_conversion(
        self, user_id: str, uuid: str, bot: str, request_body: RequestBodyClass
    ) -> bool:
        response = self.http_client.post(URL, request_body.to_dict(), HEADERS)
        self.http_client.close()

        if response.status == 200:
            self.database.add_to_whitelist(
                user_id=user_id,
                uuid=uuid,
                bot=bot,
            )
            self.database.close()
            return True
        return False
