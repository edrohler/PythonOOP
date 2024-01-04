import logging
from flask import Blueprint, Flask
from flask_restx import Api

from core.services.logging_service import LoggingService
from infrastructure.database import DatabaseConfig
from infrastructure.unit_of_work import UnitOfWork

from .endpoints.address import create_address_ns
from .endpoints.email import create_email_ns
from .endpoints.person import create_person_ns

# Configure logging
logger = LoggingService(logger_name="api", log_level="DEBUG", handler=logging.FileHandler("logs/.log"))

# Configure database
db_config = DatabaseConfig.get_instance(database_uri="sqlite:///database.db", echo=True, logger=logger)
db_config.init_db()

# Create UnitOfWork
uow = UnitOfWork.get_instance(db_config, logger)

app = Flask(__name__)

api_version = "v1"

# Register blueprint
blueprint = Blueprint('api', __name__, url_prefix=f"/api/{api_version}")
api = Api(blueprint)
api.add_namespace(create_address_ns(uow, api_version))
api.add_namespace(create_email_ns(uow, api_version))
api.add_namespace(create_person_ns(uow, api_version))
app.register_blueprint(blueprint)

# address_bp = create_address_blueprint(uow, api_version)
# app.register_blueprint(address_bp, route_prefix=f"/api/{api_version}")
# email_bp = create_email_blueprint(uow, api_version)
# app.register_blueprint(email_bp, route_prefix=f"/api/{api_version}")
# person_bp = create_person_blueprint(uow, api_version)
# app.register_blueprint(person_bp, route_prefix=f"/api/{api_version}")
