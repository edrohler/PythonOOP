import logging

class LoggingService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(LoggingService, cls).__new__(cls)
        return cls._instance

    def __init__(self, logger_name, log_level=logging.INFO, handler=None):
        if not hasattr(self, 'initialized'):  # Avoid re-initialization
            self.logger = logging.getLogger(logger_name)
            self.logger.propagate = False
            self.logger.setLevel(log_level)

            if not self.logger.handlers:
                if handler is None:
                    handler = logging.FileHandler(f'logs/{logger_name}.log')

                formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
                handler.setFormatter(formatter)
                self.logger.addHandler(handler)
                                
        self.initialized = True

    def log_info(self, message):
        self.logger.info(message)

    def log_error(self, message):
        self.logger.error(message)

    def log_warning(self, message):
        self.logger.warning(message)

    def log_debug(self, message):
        self.logger.debug(message)
