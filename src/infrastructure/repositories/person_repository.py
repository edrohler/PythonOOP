from src.infrastructure.orm.entities.person import Person
from src.infrastructure.repositories.generic_repository import GenericRepository


class PersonRepository(GenericRepository):
    def __init__(self, session, logger):
        super().__init__(session, Person, logger)
