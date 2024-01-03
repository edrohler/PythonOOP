from src.core.services.logging_service import LoggingService
from src.infrastructure.database import DatabaseConfig
from src.infrastructure.repositories.address_repository import AddressRepository
from src.infrastructure.repositories.email_repository import EmailRepository
from src.infrastructure.repositories.person_repository import PersonRepository


class UnitOfWork:
    _instance = None

    @classmethod
    def get_instance(cls, config: DatabaseConfig, logger: LoggingService):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)  # Creates a new instance
            cls._instance.initialize(config, logger)
        return cls._instance

    def initialize(self, config: DatabaseConfig, logger: LoggingService):
        if hasattr(self, '__initialized') and self.__initialized:
            logger.log_info('Unit of work already initialized')
            return
        self.__initialized = True
        self.logger = logger
        logger.log_info('Initializing unit of work')
        self.session = config.get_session()
        self.address_repository = AddressRepository(self.session, logger=config.logger)
        self.email_repository = EmailRepository(self.session, logger=config.logger)
        self.person_repository = PersonRepository(self.session, logger=config.logger)

    def __enter__(self):
        self.logger.log_info('Entering unit of work')
        return self

    def __exit__(self, type, value, traceback):
        self.logger.log_info('Exiting unit of work')
        self.session.close()
