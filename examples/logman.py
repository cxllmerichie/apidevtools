from src.apidevtools.logman import LoggerManager


LOGMAN = LoggerManager()
LOGGER = LOGMAN.add('main.log')

LOGGER.warning('test')
