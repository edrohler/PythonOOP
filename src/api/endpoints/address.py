from flask import Blueprint, request
from flask_restx import Api, Resource, Namespace, fields
from src.core.domain.viewmodels import Address

def create_address_model(api):
    return api.model('Address', {
        'address_line_1': fields.String(required=True, description='Address line 1'),
        'address_line_2': fields.String(required=False, description='Address line 2'),
        'city': fields.String(required=True, description='City'),
        'state': fields.String(required=True, description='State'),
        'zipcode': fields.String(required=True, description='Zipcode'),
        'person_id': fields.Integer(required=True, description='Person ID')
    })

def create_address_ns(api, uow, version):
    ns = Namespace(f"Adddress Endpoints", description="Address API", path=f"/api/v{version}/address")
    address_model = create_address_model(api)
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
                data = api.payload
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