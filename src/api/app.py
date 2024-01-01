from flask import Flask, Blueprint
from flask_restx import Api
from src.infrastructure.database import get_session
from src.api.endpoints.person import ns as person_ns
from src.api.endpoints.address import ns as address_ns
from src.api.endpoints.email import ns as email_ns

app = Flask(__name__)
blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint, doc='/documentation')  # Swagger documentation at /api/documentation
api.add_namespace(person_ns)
api.add_namespace(address_ns)
api.add_namespace(email_ns)
app.register_blueprint(blueprint)

if __name__ == '__main__':
    app.run(debug=True)