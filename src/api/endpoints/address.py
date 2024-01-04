from flask import Blueprint, request
from flask_restx import Api, Resource, Namespace
from src.core.domain.viewmodels import Address

def create_address_ns(uow, version):
    ns = Namespace(f"Adddress Endpoints", description="Address API", path=f"/address")
    @ns.route("/")
    class AddressList(Resource):
        def get(self):
            """Get all addresses."""
            addresses = uow.address_repository.get_all()
            return addresses
        
        def post(self):
            """Create a new address."""
            data = request.json
            address = Address(**data)
            uow.address_repository.add(address)
            uow.commit()
            return {"message": "Address created"}, 201

    @ns.route("/<int:id>")
    class AddressResource(Resource):
        def get(self, id):
            """Get an address by ID."""
            address = uow.address_repository.get_by_id(id)
            if address is None:
                return {"message": "Address not found"}, 404
            return address

        def put(self, id):
            """Update an existing address."""
            data = request.json
            uow.address_repository.update(id, **data)
            return {"message": "Address updated"}, 200

        def delete(self, id):
            """Delete an address."""
            uow.address_repository.delete(id)
            return {"message": "Address deleted"}, 200

    return ns