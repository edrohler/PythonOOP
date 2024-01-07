from src.core.domain.models.email import Email as EmailVM
from src.infrastructure.orm.entities import Email as EmailORM
from src.infrastructure.unit_of_work import UnitOfWork

class EmailService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def get_email_by_id(self, id: int) -> EmailVM:
        email_orm = self.uow.email_repository.get_by_id(id)
        email_vm = self._map_to_vm(email_orm)
        return email_vm

    def get_all_emails(self) -> list[EmailVM]:
        emails_orm = self.uow.email_repository.get_all()
        emails_vm = [self._map_to_vm(email) for email in emails_orm]
        return emails_vm

    def create_email(self, email: EmailVM):
        email_orm = self._map_to_orm(email)
        email_orm.id = None
        self.uow.email_repository.add(email_orm)
        self.uow.commit()

    def update_email(self, email: EmailVM):
        email_orm = self._map_to_orm(email)
        updated_email = self.uow.email_repository.update(email_orm)
        return updated_email

    def delete_email(self, id: int):
        email_orm = self.uow.email_repository.get_by_id(id)
        deleted_email = self.uow.email_repository.delete(email_orm)
        self.uow.commit()
        return deleted_email
        
    def _map_to_orm(self, email: EmailVM) -> EmailORM:
        # Perform the mapping logic here
        email_orm = EmailORM()
        email_orm.id = email.id
        email_orm.email_address = email.email_address
        email_orm.person_id = email.person_id
        return email_orm
    
    def _map_to_vm(self, email: EmailORM) -> EmailVM:
        email_vm = EmailVM(
            email.id
            , email.email_address
            , email.person_id
        )
        return email_vm