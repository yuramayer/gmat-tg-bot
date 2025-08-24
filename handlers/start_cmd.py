"""Bot reacts to the command /start for the everyone"""

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from db_back.users import (
    get_user_id,
    register_user
)
from back.bot_back import (
    should_reg_msg,
    registration_msg,
    already_registrated_msg
)
from back.msg_log import save_log_event
# from keyboards.menu_keyboard import menu_kb


start_cmd_router = Router()


@start_cmd_router.message(Command('start'))
async def cmd_start(message: Message, state: FSMContext):
    """Bot reacts to the /start command"""

    save_log_event(
        message=message,
        direction='inbound',
        text=message.text,
        router='start_cmd_router',
        method='cmd_start',
        event_type='command'
    )

    await state.clear()

    tg_user_id = str(message.from_user.id)

    user_db_id = await get_user_id(tg_user_id)

    msg_txt = should_reg_msg()
    message.answer(msg_txt)

    save_log_event(
        message=message,
        direction='outbound',
        text=msg_txt,
        router='start_cmd_router',
        method='cmd_start',
        event_type='message'
    )

    if user_db_id is not None:
        msg_txt = already_registrated_msg()
        message.answer(msg_txt)

        save_log_event(
            message=message,
            direction='outbound',
            text=msg_txt,
            router='start_cmd_router',
            method='cmd_start',
            event_type='message'
        )

    tg_username = None  # TODO: get username from tg
    tg_fullname = None  # TODO: get full name from tg
    await register_user(tg_user_id,
                        tg_username,
                        tg_fullname)

    msg_txt = registration_msg()
    message.answer(msg_txt)

    save_log_event(
        message=message,
        direction='outbound',
        text=msg_txt,
        router='start_cmd_router',
        method='cmd_start',
        event_type='message'
    )
