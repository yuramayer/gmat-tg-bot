"""Точка входа. create bot + start polling"""

import asyncio
from src.config import config
from src.bot.bot_factory import create_bot_dispatcher
from src.bot.utils.lifecycle import LifecycleManager


async def main():
    """Running tg bot app"""
    bot, dp = create_bot_dispatcher(config)

    lifecycle = LifecycleManager(
        admins_id=config.admins_id,
        s3_logger=dp['s3_logger']
    )

    dp.startup.register(lifecycle.on_startup)
    dp.shutdown.register(lifecycle.on_shutdown)
    await dp.start_polling(
        bot
    )


if __name__ == '__main__':
    asyncio.run(main())
