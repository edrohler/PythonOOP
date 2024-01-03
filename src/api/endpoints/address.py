from flask import Blueprint, request
from flask_restx import Api, Resource, Namespace

def create_address_blueprint(uow, version):
    address_bp = Blueprint("address", __name__)
    address_api = Api(address_bp,version=version, description="PII API")
    ns = Namespace(f"api/{version}", description="Address API")
    address_api.add_namespace(ns)

    @ns.route("/addresses")
    class AddressList(Resource):
        def get(self):
            addresses = uow.address_repository.get_all()
            return addresses
        
        def post(self):
            """Create a new address."""
            data = request.json
            address = Address(**data)
            uow.address_repository.add(address)
            uow.commit()
            return {"message": "Address created"}, 201

    @ns.route("/addresses/<int:id>")
    class Address(Resource):
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

    return address_bp