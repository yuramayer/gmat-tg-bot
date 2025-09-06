"""Config class for the project's environments"""

import os
from pathlib import Path
from dotenv import load_dotenv
from src.local_logger import LocalLogger


class Config:
    """Config loader with required/optional env variables"""

    def __init__(self, env_path: Path | None = None):
        """Initialize the Config object"""
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
        """Required variable. Raise if there's no any"""
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
        Optional variable. Returns warning 
        and default value if there's no
        any value
        """
        value = os.getenv(name, default)
        if value is None:
            self.logger.warning(
                f"⚠️ Optional environment variable not set: {name}"
                )
        return value

    def _get_bot_token(self) -> str:
        """Uploads bot token depending on the stand"""
        if self.stand == 'DEV':
            test_bot_token = self._get_required('TEST_BOT_TOKEN')
            return test_bot_token
        elif self.stand == 'PROD':
            prod_bot_token = self._get_required('PROD_BOT_TOKEN')
            return prod_bot_token
        raise EnvironmentError(
            f"❌ Stand should be 'DEV' or 'PROD'"
        )

    def _get_admin_ids(self) -> list[int]:
        """
        Load admin Telegram IDs
        from .env (required variable)
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
