import logging


logger = logging.getLogger(__name__)

logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)

logger.debug('This message should go to the log file')