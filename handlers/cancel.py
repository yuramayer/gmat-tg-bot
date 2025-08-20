"""Bot reacts to the command /start for the admins"""

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from keyboards.menu_keyboard import menu_kb
from back.msg_log import save_log_event


cancel_router = Router()


@cancel_router.message(Command('cancel'))
async def cmd_cancel(message: Message, state: FSMContext):
    """User cancels the current state"""
    save_log_event(
        message=message,
        direction='inbound',
        text=message.text,
        router='cancel_router',
        method='cmd_cancel',
        event_type='command'
    )
    await state.clear()
    msg_answer = 'Операция отменена 👌🏻'
    await message.answer(msg_answer,
                         reply_markup=menu_kb())

    save_log_event(
        message=message,
        direction='outbound',
        text=msg_answer,
        router='cancel_router',
        method='cmd_cancel',
        event_type='message'
    )
