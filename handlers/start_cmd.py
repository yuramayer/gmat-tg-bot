"""Bot reacts to the command /start to the everyone"""

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from back.db_back import user_exists, add_user
from back.bot_back import create_start_message
from back.msg_log import save_log_event
from keyboards.menu_keyboard import menu_kb


start_cmd_router = Router()


@start_cmd_router.message(Command('start'))
async def cmd_start(message: Message, state: FSMContext):
    """Bot says hi to new user"""

    save_log_event(
        message=message,
        direction='inbound',
        text=message.text,
        router='start_cmd_router',
        method='cmd_start',
        event_type='command'
    )

    await state.clear()
    chat_id = str(message.from_user.id)
    if not user_exists(chat_id):
        add_user(chat_id)
        msg_answer = 'Словарь готов к работе 💫'
        await message.answer(msg_answer)

        save_log_event(
            message=message,
            direction='outbound',
            text=msg_answer,
            router='start_cmd_router',
            method='cmd_start',
            event_type='message'
        )

    msg_answer = create_start_message()
    await message.answer(msg_answer, reply_markup=menu_kb())

    save_log_event(
        message=message,
        direction='outbound',
        text=msg_answer,
        router='start_cmd_router',
        method='cmd_start',
        event_type='message'
    )
