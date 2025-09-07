"""Config class for the project's environments"""

import os
from pathlib import Path
from dotenv import load_dotenv
from src.local_logger import LocalLogger


class Config:
    """Config loader with required/optional env variables"""

    def __init__(self, env_path: Path | None = None):
        """
        Initialize the Config object

        Args:
            env_path (pathlib.Path, optional): path to the .env file
        """
        env_file = env_path or Path(".env")
        load_dotenv(dotenv_path=env_file, override=True)

        self.logger = LocalLogger("config_logger")

        self.stand = self._get_required('STAND')

        self.bot_token = self._get_bot_token()

        self.cloud_s3_id_key = self._get_required(
            'CLOUD_S3_ID_KEY')
        self.cloud_s3_secret_key = self._get_required(
            'CLOUD_S3_SECRET_KEY')
        self.bucket_name = self._get_required(
            'BUCKET_NAME')

        self.admins_id = self._get_admin_ids()

        self.db_host = self._get_required('DB_HOST')
        self.db_name = self._get_required('DB_NAME')
        self.db_port = self._get_required('DB_PORT')
        self.db_user = self._get_required('DB_USER')
        self.db_pass = self._get_required('DB_PASS')

    def _get_required(self, name: str) -> str:
        """
        Required variable to upload. Raise if there's no any

        Args:
            name (str): name of the environment variable

        Returns:
            str: current value for the env variable

        Raises:
            EnvironmentError: if there's no any environmental variable
                with such name
        """
        value = os.getenv(name)
        if value is None:
            raise EnvironmentError(
                f"❌ Missing required environment variable: {name}"
                )
        return value

    def _get_optional(
            self,
            name: str,
            default: str | None = None
            ) -> str | None:
        """
        Optional variable to upload. Returns warning
        and default value if there's no any value

        Args:
            name (str): name of the environment variable
            default (str, optional): default value for the variables
                if there's no any value in .env file for this var

        Returns:
            str: value for the environment var
        """
        value = os.getenv(name, default)
        if value is None:
            self.logger.warning(
                f"⚠️ Optional environment variable not set: {name}"
                )
        return value

    def _get_bot_token(self) -> str:
        """
        Uploads bot token depending on the stand

        Returns:
            str: value for the 'stand' environment:
                should be 'DEV' or 'PROD' in the .env

        Raises:
            EnvironmentError: if the environment variable
                has any value then 'DEV' ors 'PROD'
        """
        if self.stand == 'DEV':
            test_bot_token = self._get_required('TEST_BOT_TOKEN')
            return test_bot_token
        if self.stand == 'PROD':
            prod_bot_token = self._get_required('PROD_BOT_TOKEN')
            return prod_bot_token
        raise EnvironmentError(
            "❌ Stand should be 'DEV' or 'PROD'"
        )

    def _get_admin_ids(self) -> list[int]:
        """
        Load admin Telegram IDs
        from .env (required variable)

        Returns:
            list[int]: list of integers
                with tg id's of the bot's admins

        Raises:
            ValueError: if any of the admin's id's
                contains non-integers in the '.env' file
            RuntimeError: if there's no any integer
                in the ADMINS var in .env file
        """
        admins_ids_str = self._get_required("ADMINS")

        try:
            admins = [
                int(admin_id.strip())
                for admin_id in admins_ids_str.split(",")
                if admin_id.strip()
            ]
        except ValueError as exc:
            self.logger.error(
                "Invalid value in ADMINS: %s", admins_ids_str)
            raise ValueError(
                f"ADMINS contains non-integer values: {admins_ids_str}"
            ) from exc

        if not admins:
            self.logger.error(
                "ADMINS is empty or contains no valid IDs")
            raise RuntimeError(
                "ADMINS must contain at least one valid integer ID")

        self.logger.info("Loaded ADMINS: %s", admins)
        return admins


config = Config()
