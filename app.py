"""Starting Telegram bot app"""

import asyncio
from utils.starting import on_startup
from handlers import (
    start_cmd_router, send_words_router,
    add_word_router, cancel_router, all_words_router,
    plug_router
)
from bot import bot, dp


async def main():
    """Bot startup function"""
    dp.include_routers(cancel_router, start_cmd_router,
                       all_words_router, send_words_router,
                       add_word_router, plug_router)
    dp.startup.register(on_startup)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
