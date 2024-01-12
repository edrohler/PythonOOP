from flask import request
from flask_restx import Resource, Namespace
from src.api.utils import schema_to_api_model
from src.core.serialization.address import AddressSchema
from src.core.services.logging_service import LoggingService
from src.core.services.address_service import AddressService
from src.infrastructure.unit_of_work import UnitOfWork

def create_address_ns(api, uow: UnitOfWork, version, logger: LoggingService):
    ns = Namespace(f"Address Endpoints", description="Address API", path=f"/api/v{version}/address")
    address_model = schema_to_api_model(AddressSchema, api)
    address_service = AddressService(uow)
    @ns.route("/")
    class AddressList(Resource):
        def get(self):
            """Get all addresses."""
            addresses = address_service.get_all_addresses()
            return AddressSchema(many=True).dump(addresses)
        
        @ns.expect(address_model, validate=True)
        def post(self):
            """Create a new address."""
            try:
                address = AddressSchema().load(request.json)
                address_service.create_address(address)
                return {"message": "Address created"}, 201
            except Exception as e:
                logger.log_error(e)
                return {"message": "An Error Occurred"}, 400
        
        @ns.expect(address_model, validate=True)
        def put(self):
            """Update an existing address."""
            if "id" == None or "id" not in request.json:
                return {"message": "Id is required"}, 400
            try:
                address = AddressSchema().load(request.json)
                updated_address = address_service.update_address(address)
                if updated_address is None:
                    return {"message": "Error updating address"}, 400
                return {"message": "Address updated"}, 200
            except Exception as e:
                logger.log_error(e)
                return {"message": "Error updating address"}, 400
        
    @ns.route("/<int:id>")
    class AddressResource(Resource):
        def get(self, id):
            """Get an address by ID."""
            address = address_service.get_address_by_id(id)
            if address is None:
                return {"message": "Address not found"}, 404
            return AddressSchema().dump(address)


        def delete(self, id):
            """Delete an address."""
            try:
                deleted_address = address_service.delete_address(id)
                if deleted_address is None:
                    return {"message": "Address not found"}, 404
                return {"message": f"Address with id: {id} deleted"}, 200
            except Exception as e:
                logger.log_error(e)
                return {"message": "Error deleting address"}, 400

    return ns