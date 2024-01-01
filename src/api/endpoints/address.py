from flask_restx import Resource, Namespace

ns = Namespace('api', description='API for CRUD operations', version=1.0)

@ns.route("/address")
class AddressList(Resource):
    def get(self):
        return "List of addresses"