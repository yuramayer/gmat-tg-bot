"""Bot functionality on the startup and end"""

from aiogram import Bot
from src.local_logger import LocalLogger
from src.bot.s3_logging.s3_logger import S3Logger


class LifecycleManager:
    """Manage startup/shutdown lifecycle of the bot"""

    def __init__(
            self,
            admins_id: list[int],
            s3_logger: S3Logger,
            ):
        """
        Initialize lifecycle manager

        admin_ids (list[int]): admins' tg ids
        s3_logger (S3Logger): S3 cloud logger object
        """
        self.admins_id = admins_id
        self.s3_logger = s3_logger
        self.local_logger = LocalLogger(
            name="lifecycle_logger"
            )

    async def on_startup(
            self,
            bot: Bot
            ):
        """
        Notify bot admins when bot starts

        Args:
            bot (aiogram.Bot): aiogram bot object
        """
        self.local_logger.info('Starting on_startup func')
        for admin_id in self.admins_id:
            try:
                await bot.send_message(
                    admin_id,
                    "The bot is started and ready!"
                    )
                msg_finish = (
                    f"Notified admin {admin_id} "
                    "on startup successfully!"
                )
                self.local_logger.info(
                    msg_finish
                )
            except Exception as err:
                msg_error = (
                    f"Failed to notify admin {admin_id} "
                    f"on startup: {err}"
                )
                self.local_logger.error(
                    msg_error
                )

    async def on_shutdown(self, bot: Bot):
        """
        Called when bot stops

        Args:
            bot (aiogram.Bot): aiogram bot object
        """
        for admin_id in self.admins_id:
            try:
                await bot.send_message(
                    admin_id,
                    "The bot is stopped!"
                    )
                msg_finish = (
                    f"Notified admin {admin_id} "
                    "on shutdown successfully!"
                )
                self.local_logger.info(
                    msg_finish
                )
            except Exception as err:
                msg_error = (
                    f"Failed to notify admin {admin_id} "
                    f"on shutdown: {err}"
                )
                self.local_logger.error(
                    msg_error
                )
