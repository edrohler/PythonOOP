import logging

class LoggingService:
    def __init__(self, logger_name, log_level=logging.INFO):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(log_level)
        handler = logging.FileHandler(f'logs/{logger_name}.log')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def log_info(self, message):
        self.logger.info(message)

    def log_error(self, message):
        self.logger.error(message)

    def log_warning(self, message):
        self.logger.warning(message)

    def log_debug(self, message):
        self.logger.debug(message)