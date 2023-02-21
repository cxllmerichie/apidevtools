from loguru import logger as _logger
from loguru._logger import Logger
from sys import stderr as _stderr


class LoggerManager:
    def __init__(self, format: str = '{level.icon} <yellow>|</yellow> '
                                     '<blue>{time:YYYY-MM-DD HH:mm:ss}</blue> '
                                     '<yellow>|</yellow> {level.name} - {message}'):
        _logger.configure(handlers=[{'sink': _stderr, 'format': format}])
        self.__logger_format = format

    def add(self, name: str, path: str, rotation: str = '20 MB', retention: str = '30 days') -> Logger:
        _logger.add(path, enqueue=True, backtrace=True, diagnose=True, format=self.__logger_format,
                    rotation=rotation, retention=retention, filter=lambda r: name in r['extra'])
        logger = _logger.bind(**{name: True})
        setattr(self, name, logger)
        return logger
