from .database import get_session, DatabaseConfig
from .repositories import AddressRepository, EmailRepository, PersonRepository

class UnitOfWork:
    def __init__(self, config: DatabaseConfig):
        self.session = config.get_session()
        self.address_repository = AddressRepository(self.session, logger=config.logger)
        self.email_repository = EmailRepository(self.session, logger=config.logger)
        self.person_repository = PersonRepository(self.session, logger=config.logger)
        
    def __enter__(self):
        return self
    
    def __exit__(self, type, value, traceback):
        self.session.close()