"""Methods for the logging the bot's messages"""

from datetime import datetime, timezone
from dataclasses import dataclass, field
from aiogram.types import Message
from back.cloud import get_log_key, send_logs


# pylint: disable=too-many-instance-attributes
@dataclass
class MessageLog:
    """
    Structured data object representing bot interaction event

    :param timestamp: ISO UTC timestamp of the message,
        default value - current timestamp
    :param chat_id: TG message chat id
    :param message_id: ID of the message in the Telegram
    :param direction: Direction of the message,
        should be 'inbound' (from user)
        or 'outbound' (from the bot)
    :param text: Content of the message
    :param router: Bot's router that handled the message
    :param method: Bot's method or handler name
    :param event_type: Type of the interaction:
        "message", "command", "error", etc
    """
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat())
    chat_id: int
    message_id: int
    direction: str
    text: str
    router: str
    method: str
    event_type: str


def create_log_json(
        log: MessageLog) -> dict:
    """
    Converts MessageLog object into dict for logging

    :param log: MessageLog dataclass instance with context
    :return: Dictionary for S3 Storage uploading
    """
    log_dict = {
        'timestamp': log.timestamp,
        'chat_id': log.chat_id,
        'message_id': log.message_id,
        'direction': log.direction,
        'text': log.text,
        'router': log.router,
        'method': log.method,
        'event_type': log.event_type
    }
    return log_dict


def save_log_event(
        *,
        message: Message,
        direction: str,
        text: str,
        router: str,
        method: str,
        event_type: str
        ):
    """
    Log an event by constructing structured entry and dispatching it to the S3

    :param message: aiogram.types.Message object from the user
    :param direction: Direction of the message,
        'inbound' (from user) or 'outbound' (from bot)
    :param text: Text of the message to be logged
    :param router: Name of the Router that handled this message
    :param method: Name of the handler method invoked
    :param event_type: Type of the interaction,
        "message", "command", "error", etc.
    """
    log_obj = MessageLog(
        chat_id=message.chat.id,
        message_id=message.message_id,
        direction=direction,
        text=text,
        router=router,
        method=method,
        event_type=event_type
    )
    log_json = create_log_json(log_obj)
    time_now = datetime.now().isoformat()
    log_key = get_log_key(time_now, message.chat.id)
    send_logs(log_json, log_key)
