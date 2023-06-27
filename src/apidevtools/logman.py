from loguru._logger import Logger
from loguru import logger
import sys as _sys
import os as _os


format = '{level.icon} <yellow>|</yellow> ' \
          '<blue>{time:YYYY-MM-DD HH:mm:ss}</blue> <yellow>|</yellow> ' \
          '<level>{level.name} - {message}</level>'
logger.configure(handlers=[{'sink': _sys.stderr, 'format': format}])


def add(filepath: str) -> Logger:
    name = filepath
    if filepath.endswith('.log'):
        name = _os.path.basename(filepath).rstrip('.log')
    else:
        filepath = f'{filepath}.log'
    logger.add(
        filepath, enqueue=True, backtrace=True, diagnose=True, format=format, filter=lambda r: name in r['extra']
    )
    return logger.bind(**{name: True})
