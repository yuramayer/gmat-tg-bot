"""Bot couldn't read the message from user"""

from aiogram import Router
from aiogram.types import Message
from keyboards.menu_keyboard import menu_kb
from back.bot_back import create_plug_message
from back.msg_log import save_log_event


plug_router = Router()


@plug_router.message()
async def plug_msg(message: Message):
    """Bot couldn't understand user, asks with menu"""

    save_log_event(
        message=message,
        direction='inbound',
        text=message.text,
        router='plug_router',
        method='plug_msg',
        event_type='command'
    )

    msg_answer = create_plug_message()
    await message.answer(msg_answer,
                         reply_markup=menu_kb())

    save_log_event(
        message=message,
        direction='outbound',
        text=msg_answer,
        router='plug_router',
        method='plug_msg',
        event_type='message'
    )
