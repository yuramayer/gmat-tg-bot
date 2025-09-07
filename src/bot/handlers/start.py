"""Start command handler"""

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from src.bot.s3_logging.s3_logger import S3Logger

start_router = Router()


@start_router.message(Command('start'))
async def cmd_start(
    message: Message,
    s3_logger: S3Logger
    ):
    """Handle /start command & log it"""

    s3_logger.log_message(
        message=Message,
        direction='inbound',
        text=message.text,
        router='start_router',
        method='cmd_start',
        event_type='command'
    )

    msg_answer = 'Hi!'
    await message.answer('Hi!')

    s3_logger.log_message(
        message=Message,
        direction='outbound',
        text=msg_answer,
        router='start_router',
        method='cmd_start',
        event_type='command'
    )
