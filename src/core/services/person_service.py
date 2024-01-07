from src.core.domain.models.person import Person as PersonVM
from src.infrastructure.orm.entities import Person as PersonORM
from src.infrastructure.repositories.person_repository import PersonRepository
from src.infrastructure.unit_of_work import UnitOfWork

class PersonService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def get_person_by_id(self, id: int) -> PersonVM:
        person_orm = self.uow.person_repository.get_by_id(id)
        person_vm = self._map_to_vm(person_orm)
        return person_vm

    def get_all_people(self) -> list[PersonVM]:
        people_orm = self.uow.person_repository.get_all()
        people_vm = [self._map_to_vm(person) for person in people_orm]
        return people_vm

    def create_person(self, person: PersonVM):
        person_orm = self._map_to_orm(person)
        person_orm.id = None
        self.uow.person_repository.add(person_orm)
        self.uow.commit()

    def update_person(self, person: PersonVM):
        person_orm = self._map_to_orm(person)
        updated_person = self.uow.person_repository.update(person_orm)
        return updated_person

    def delete_person(self, id: int):
        person_orm = self.uow.person_repository.get_by_id(id)
        self.uow.person_repository.delete(person_orm)
        self.uow.commit()

    def _map_to_orm(self, person: PersonVM) -> PersonORM:
        # Perform the mapping logic here
        person_orm = PersonORM()
        person_orm.id = person.id
        person_orm.first_name = person.first_name
        person_orm.last_name = person.last_name
        person_orm.gender = person.gender
        person_orm.age = person.age
        return person_orm
    
    def _map_to_vm(self, person: PersonORM) -> PersonVM:
        person_vm = PersonVM(
            person.id
            , person.first_name
            , person.last_name
            , person.gender
            , person.age
        )
        return person_vm
