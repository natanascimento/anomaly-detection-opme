import os
from datetime import datetime
import logging

from core.config import settings


class ConsoleHandler:
    
    @staticmethod
    def create(formatter: logging.Formatter, level: logging = logging.DEBUG):
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        return console_handler
    

class FileHandler:
  
    @staticmethod
    def create(formatter: logging.Formatter, level: logging = logging.DEBUG):

        if not os.path.exists(settings.app.LOGS_PATH):
            os.makedirs(settings.app.LOGS_PATH)

        console_handler = logging.FileHandler(f"{settings.app.LOGS_PATH}/{datetime.now()}.log")
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        return console_handler