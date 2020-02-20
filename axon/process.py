import logging


class Process(object):
    name = None

    def __init__(self):
        self.logger = logging.getLogger(self.name)

    def info(self, *args, **kwargs):
        self.logger.log(*args, **kwargs)

    def warning(self, *args, **kwargs):
        self.logger.warning(*args, **kwargs)

    def error(self, *args, **kwargs):
        self.logger.error(*args, **kwargs)

    def critical(self, *args, **kwargs):
        self.logger.critical(*args, **kwargs)
