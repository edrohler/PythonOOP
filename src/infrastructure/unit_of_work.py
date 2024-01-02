from src.core.services.logging_service import LoggingService
from .database import get_session, DatabaseConfig
from .repositories import AddressRepository, EmailRepository, PersonRepository

class UnitOfWork:
    def __init__(self, config: DatabaseConfig, logger: LoggingService):
        self.logger = logger
        logger.log_info('Creating new unit of work')
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