import logging


logger = logging.getLogger(__name__)

logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)

class Log:
	def log(self, а):
		logger.debug(а)