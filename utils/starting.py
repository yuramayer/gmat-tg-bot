"""Methods running when the bot is starting"""

from aiogram.exceptions import TelegramBadRequest
from bot import bot
from config.conf import admins_ids, DB_PATH
from back.db_back import is_checked_db, create_tables


async def on_startup():
    """When bot is started, check db & send message to the admins"""

    for admin_id in admins_ids:
        try:
            await bot.send_message(admin_id, 'Бот включён 😎')
        except TelegramBadRequest:
            print(f"Couldn't send message to the id: {admin_id}")

    if not is_checked_db():
        with open(DB_PATH, 'w', encoding='utf-8') as db:
            db.close()  # Создаём пустую БД, если файла нет
    create_tables()

    for admin_id in admins_ids:
        try:
            await bot.send_message(admin_id, 'База успешно подключена ✌🏻')
        except TelegramBadRequest:
            print(f"Couldn't send message to the id: {admin_id}")
