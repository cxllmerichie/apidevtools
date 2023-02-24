from apidevtools.logman import LoggerManager


LM = LoggerManager()
LOGGER = LM.add('MAIN', 'main.log')

LM.MAIN.warning('Test')
LOGGER.warning('Test')
