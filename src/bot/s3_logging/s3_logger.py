"""Wrapper for structured logging into S3"""

from datetime import datetime, timezone
from dataclasses import dataclass, field, asdict
from aiogram.types import Message
from src.bot.s3_logging.client import S3Client
from src.local_logger import LocalLogger


@dataclass
class MessageLog:
    """
    Structured data object
    representing bot interaction event
    """
    timestamp: str = field(
        default_factory=lambda: datetime.now(
            timezone.utc
        ).isoformat()
    )
    chat_id: int = 0
    message_id: int = 0
    direction: str = ""
    text: str = ""
    router: str = ""
    method: str = ""
    event_type: str = ""


class S3Logger:
    """
    High-level logger that serialized & uploads
    bot events into S3
    """
    def __init__(self, s3_client: S3Client):
        """
        Args:
            s3_client: initialized S3Client instance
        """
        self._s3_client = s3_client
        self.logger = LocalLogger("s3logger_logger")
        self.logger.info('The S3 logger is initialized')

    def log_message(
            self,
            *,
            message: Message,
            direction: str,
            text: str,
            router: str,
            method: str,
            event_type: str
        ) -> None:
        """
        Log the action & send the log to the S3

        Args:
            message (aiogram.types.Message): TG
                message that connected with log
            direction (str): type of the message,
                should be inbound or outbound
            text (str): text for the log
            router (str): name of the router
                where the event happened
            method (str): name of the func
                where the event happened
            event_type (str): type of the action
        """
        log_obj = MessageLog(
            chat_id=message.chat.id,
            message_id = message.message_id,
            direction=direction,
            text=text,
            router=router,
            method=method,
            event_type=event_type
        )
        log_dict = asdict(log_obj)
        log_key = self._s3_client.get_log_key(
            datetime.now().isoformat(),
            message.chat.id
        )
        self._s3_client.send_logs(
            log_dict, log_key
        )
