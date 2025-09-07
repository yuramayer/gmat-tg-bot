"""Local logger class"""

import logging


class LocalLogger:
    """Custom wrapper arount python logging.Logger"""

    def __init__(
            self,
            name: str = "local_logger",
            level: int = logging.INFO
            ):
        """
        Initialize logger object

        Args:
            name (str, optional): name for the current logger,
                default = 'local_logger'
            level (int, optional): logging level,
                default = 'INFO'
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # check for not dublicate
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s [%(levelname)s] "
                "%(name)s: %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def debug(self, msg: str, *args, **kwargs) -> None:
        """
        Debug logger method

        Args:
            msg (str): message to log
        """
        self.logger.debug(msg, *args, **kwargs)

    def info(self, msg: str, *args, **kwargs) -> None:
        """
        Info logger method

        Args:
            msg (str): message to log
        """
        self.logger.info(msg, *args, **kwargs)

    def warning(self, msg: str, *args, **kwargs) -> None:
        """
        Warning logger method

        Args:
            msg (str): message to log
        """
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg: str, *args, **kwargs) -> None:
        """
        'Error message' logger method

        Args:
            msg (str): message to log
        """
        self.logger.error(msg, *args, **kwargs)

    def critical(self, msg: str, *args, **kwargs) -> None:
        """
        'Critical message' logger method

        Args:
            msg (str): message to log
        """
        self.logger.critical(msg, *args, **kwargs)
