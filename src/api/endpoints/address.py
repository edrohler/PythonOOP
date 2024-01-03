from flask_restx import Resource, Namespace

def create_address_namespace(uow):
    ns = Namespace('api', description='API for CRUD operations', version=1.0)

    @ns.route("/address")
    class AddressList(Resource):
        def get(self):
            addresses = uow.address_repository.get_all()
            return addresses
        
    return ns