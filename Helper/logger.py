import logging


logger = logging.getLogger(__name__)
Format = '%(asctime)s %(clientip)-15s %(user)-8s %(message)s'
logging.basicConfig(format=Format,filename='.\logs\status.log', encoding='utf-8', level=logging.INFO)

class Log:
	def log(self, а):
		logger.info(а)