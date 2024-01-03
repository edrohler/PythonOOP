import logging

class LoggingService:
    _instance = None  # Class attribute to hold the singleton instance

    @classmethod
    def get_instance(cls, logger_name, log_level=logging.INFO, handler=None):
        """ Class method to get the singleton instance of the class. """
        if cls._instance is None:
            cls._instance = cls(logger_name, log_level, handler)
        return cls._instance

    def __init__(self, logger_name, log_level, handler):
        """ Constructor is made private to prevent direct instantiation. """
        if not hasattr(self, 'initialized'):  # Avoid re-initialization
            self.logger = logging.getLogger(logger_name)
            self.logger.propagate = False
            self.logger.setLevel(log_level)

            # Clear existing handlers
            if self.logger.handlers:
                self.logger.handlers = []

            # Add new handler
            if handler is None:
                handler = logging.FileHandler(f'logs/{logger_name}.log')

            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

            self.initialized = True
            self.logger.info('LoggingService initialized')

    def log_info(self, message):
        self.logger.info(message)

    def log_error(self, message):
        self.logger.error(message)

    def log_warning(self, message):
        self.logger.warning(message)

    def log_debug(self, message):
        self.logger.debug(message)
