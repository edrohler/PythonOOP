from flask import request
from flask_restx import Resource, Namespace
from src.api.schemas.address import AddressSchema
from src.api.utils import schema_to_api_model
from src.core.domain.models import Address
from src.core.services.logging_service import LoggingService

def create_address_ns(api, uow, version, logger: LoggingService):
    ns = Namespace(f"Adddress Endpoints", description="Address API", path=f"/api/v{version}/address")
    address_model = schema_to_api_model(AddressSchema, api)
    @ns.route("/")
    class AddressList(Resource):
        def get(self):
            """Get all addresses."""
            addresses = uow.address_repository.get_all()
            return addresses
        @ns.expect(address_model, validate=True)
        def post(self):
            """Create a new address."""
            try:
                data = AddressSchema().load(request.json)
                address = Address(**data)
                uow.address_repository.add(address)
                uow.commit()
                return {"message": "Address created"}, 201
            except Exception as e:
                return {"message": str(e)}, 400

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
            data = api.payload
            uow.address_repository.update(id, **data)
            return {"message": "Address updated"}, 200

        def delete(self, id):
            """Delete an address."""
            uow.address_repository.delete(id)
            return {"message": "Address deleted"}, 200

    return ns