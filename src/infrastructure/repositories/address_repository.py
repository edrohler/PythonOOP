from src.infrastructure.orm.entities.address import Address
from src.infrastructure.repositories.generic_repository import GenericRepository

class AddressRepository(GenericRepository):
    def __init__(self, session, logger):
        super().__init__(session, Address, logger)