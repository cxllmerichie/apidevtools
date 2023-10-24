from loguru._logger import Logger
from loguru import logger
import sys as _sys
import os as _os


format = '<level>{level.icon} {level.name}</level> <yellow>|</yellow> ' \
          '<blue>{time:YYYY-MM-DD HH:mm:ss}</blue> <yellow>|</yellow> ' \
          '<level><cyan>{name}</cyan>:<cyan>{function}</cyan> - {message}</level>'
logger.configure(handlers=[{'sink': _sys.stderr, 'format': format}])


def add(filepath: str) -> Logger:
    name = _os.path.basename(filepath).rstrip('.log')
    logger.add(
        # level=level,  # TRACE & DEBUG are not supposed to be saved in log files
        format=format,  # formatting
        sink=filepath,  # save to file
        enqueue=True,  # async
        backtrace=True,  # affects logger.exception only
        diagnose=True,  # detailed formatting?
        catch=True,  # log errors caught when logging other errors
    )
    return logger.bind(**{name: True})