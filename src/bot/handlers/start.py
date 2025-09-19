"""Start command handler"""

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from src.bot.s3_logging.s3_logger import S3Logger
from src.bot.services.user_service import UserService

start_router = Router()


@start_router.message(Command('start'))
async def cmd_start(
    message: Message,
    session: AsyncSession,
    s3_logger: S3Logger
):
    """Handle /start command & log it"""

    s3_logger.log_message(
        message=message,
        direction='inbound',
        text=message.text,
        router='start_router',
        method='cmd_start',
        event_type='command'
    )

    service = UserService(session)
    user = await service.get_or_create(
        message.from_user.id, message.from_user.first_name
    )
    msg_answer = f'Hi, {user.name}!'
    await message.answer(msg_answer)

    s3_logger.log_message(
        message=message,
        direction='outbound',
        text=msg_answer,
        router='start_router',
        method='cmd_start',
        event_type='command'
    )
