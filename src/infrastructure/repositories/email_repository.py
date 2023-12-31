from src.infrastructure.orm.entities.email import Email
from src.infrastructure.repositories.generic_repository import GenericRepository

class EmailRepository(GenericRepository):
    def __init__(self, session):
        super().__init__(session, Email)