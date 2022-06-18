
import logging
import datetime
import os

class Log(object):

    log = None

    def __init__(self, name):
        self.name = name

        if not os.path.isdir('./logs'):
            os.mkdir('./logs')

        Log.log = self.setup_custom_logger()

    def setup_custom_logger(self):
        formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')

        streamhandler = logging.StreamHandler()
        streamhandler.setFormatter(formatter)

        today = datetime.date.today()
        log_filename = f'{today}.log'

        filehandler = logging.FileHandler(f'./logs/{log_filename}')
        filehandler.setFormatter(formatter)

        logger = logging.getLogger(self.name)
        logger.setLevel(logging.INFO)
        logger.addHandler(streamhandler)
        logger.addHandler(filehandler)
        return logger

    @staticmethod
    def logger() -> logging.Logger:
        return Log.log
