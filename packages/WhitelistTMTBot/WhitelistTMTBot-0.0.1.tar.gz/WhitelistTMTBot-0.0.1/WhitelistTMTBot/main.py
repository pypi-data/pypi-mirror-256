from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from dbase import AsyncDatabase
from server import AsyncHTTPClient


class BotHandler:
    def __init__(self, token, db_file):
        self.bot = Bot(token=token, parse_mode="HTML")
        self.dp = Dispatcher(self.bot, storage=MemoryStorage())
        self.db = AsyncDatabase(db_file)
        self.http_client = AsyncHTTPClient()
        self.register_handlers()

    async def on_startup(self, _):
        await self.db.connect()
        await self.db.create_whitelist_table()
        print("Bot started and database initialized.")

    async def on_shutdown(self, _):
        await self.db.close()
        await self.http_client.close()
        print("Bot shutdown")

    def register_handlers(self):
        @self.dp.message_handler(commands=['start'])
        async def start(message: types.Message):
            user_id = message.from_user.id
            # Проверяем, есть ли пользователь в таблице whitelist
            user_exists = await self.db.check_user_in_whitelist(user_id)

            if user_exists:
                await message.answer("Вы уже зарегистрированы в системе.")
            else:
                # Продолжение существующей логики, если пользователя нет в таблице
                print("message", message)
                current_bot = await self.bot.get_me()
                data = {
                    "user_uuid": message.get_args(),
                    "telegram_bot_username": current_bot.username,
                    "telegram_user_id": message.from_user.id,
                    "telegram_user_username": message.from_user.username,
                    "telegram_user_fullname": (
                        f"{message.from_user.first_name} {message.from_user.last_name}"
                        if message.from_user.last_name
                        else message.from_user.first_name
                    ),
                }

                url = "https://events.tmtsocket.com/event/bot-activated/"
                headers = {"Content-Type": "application/json"}

                # Отправляем POST запрос
                response = await self.http_client.post(url, data, headers)

                # Проверка статуса ответа
                if response.status == 200:
                    # Если статус ответа равен 200, добавляем пользователя в whitelist
                    await self.db.add_to_whitelist(
                        user_id=message.from_user.id,
                        uuid=data["user_uuid"],
                        bot=current_bot.username,
                    )
                    await message.answer(f"User {message.from_user.username} added to whitelist.")
                else:
                    # Обработка других статусов ответа
                    await message.answer(f"Error: {response.status}")

    def run(self):
        executor.start_polling(
            self.dp,
            skip_updates=True,
            on_startup=self.on_startup,
            on_shutdown=self.on_shutdown,
        )


if __name__ == "__main__":
    TOKEN = "6320433601:AAH-b3EytTEL46-FalmLK0WlvV--hY9YMWg"
    DB_FILE = "whitelist.db"
    bot_handler = BotHandler(token=TOKEN, db_file=DB_FILE)
    bot_handler.run()
