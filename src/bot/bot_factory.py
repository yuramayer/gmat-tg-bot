"""Создание Bot и Dispatcher"""

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from src.bot.s3_logging.client import S3Client
from src.bot.s3_logging.s3_logger import S3Logger
from src.config.config import Config


def create_bot_dispatcher(
        config: Config
        ) -> tuple[Bot, Dispatcher]:
    """
    Initialize bot & dispatcher
    aiogram objects

    Args:
        config (Config): Config loader for the app
    
    Returns:
        tuple: Aiogram Bot & Dispatcher objects
    """
    bot = Bot(
        token=config.bot_token,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML
        )
    )
    dp = Dispatcher(storage=MemoryStorage())

    s3_client = S3Client(
        access_key=config.cloud_s3_id_key,
        secret_key=config.cloud_s3_secret_key,
        bucket_name=config.bucket_name
    )
    s3_logger = S3Logger(
        s3_client
    )

    dp['config'] = config
    dp['s3_logger'] = s3_logger

    from src.bot.handlers import start_router
    dp.include_router(start_router)

    return bot, dp
