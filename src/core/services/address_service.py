from src.core.domain.models.address import Address as AddressVM
from src.infrastructure.orm.entities import Address as AddressORM
from src.infrastructure.unit_of_work import UnitOfWork

class AddressService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def get_address_by_id(self, id: int) -> AddressVM:
        address_orm = self.uow.address_repository.get_by_id(id)
        address_vm = self._map_to_vm(address_orm)
        return address_vm

    def get_all_addresses(self) -> list[AddressVM]:
        addresses_orm = self.uow.address_repository.get_all()
        addresses_vm = [self._map_to_vm(address) for address in addresses_orm]
        return addresses_vm

    def create_address(self, address: AddressVM):
        address_orm = self._map_to_orm(address)
        address_orm.id = None
        self.uow.address_repository.add(address_orm)

    def update_address(self, address: AddressVM):
        address_orm = self._map_to_orm(address)
        updated_address = self.uow.address_repository.update(address_orm)
        return updated_address

    def delete_address(self, id: int):
        address_orm = self.uow.address_repository.get_by_id(id)
        deleted_address = self.uow.address_repository.delete(address_orm)
        return deleted_address
        
    def _map_to_orm(self, address: AddressVM) -> AddressORM:
        # Perform the mapping logic here
        address_orm = AddressORM()
        address_orm.id = address.id
        address_orm.address_line_1 = address.address_line_1
        address_orm.address_line_2 = address.address_line_2
        address_orm.city = address.city
        address_orm.state = address.state
        address_orm.zip_code = address.zip_code
        address_orm.person_id = address.person_id
        return address_orm
    
    def _map_to_vm(self, address: AddressORM) -> AddressVM:
        address_vm = AddressVM(
            address.id
            , address.address_line_1
            , address.address_line_2
            , address.city
            , address.state
            , address.zip_code
            , address.person_id
        )
        return address_vm
