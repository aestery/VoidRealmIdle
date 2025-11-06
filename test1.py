import logging


class Logger:
    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.logger.info(self.logger.name)
    
    def get_loffer_name(self):
        print(self.logger.name)

