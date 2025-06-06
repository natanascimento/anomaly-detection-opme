import logging

from core.logging.config import LoggerConfig 
from core.logging.handlers import ConsoleHandler, FileHandler


class APILogger:
    
    @staticmethod
    def _set_logger(
        name: str, handlers: list[logging.Handler], level: logging = logging.DEBUG
    ):
        logger = logging.getLogger(name)
        logger.setLevel(level)
        if logger.hasHandlers():
            logger.handlers.clear()
        for handler in handlers:
            logger.addHandler(handler)
        return logger


    def get(self, logger=LoggerConfig):
        logger = self._set_logger(
            name=logger.name,
            handlers=[
                ConsoleHandler().create(
                    formatter=logging.Formatter(fmt=logger.formatt),
                    level=logger.level
                ),
                FileHandler().create(
                    formatter=logging.Formatter(fmt=logger.formatt),
                    level=logger.level
                )
            ],
            level=logger.level,
        )
        return logger
