import logging
from flask import Blueprint, Flask
from flask_restx import Api

from core.services.logging_service import LoggingService
from infrastructure.database import DatabaseConfig
from infrastructure.unit_of_work import UnitOfWork

from .endpoints.address import create_address_ns
from .endpoints.email import create_email_ns
from .endpoints.person import create_person_ns

def create_app(debug=False, use_reloader=False, database_uri="sqlite:///database.db", echo=True, log_level="DEBUG"):
    # Configure logging
    logger = LoggingService(logger_name="api", log_level=log_level, handler=logging.FileHandler("logs/.log"))

    # Configure database
    db_config = DatabaseConfig.get_instance(database_uri=database_uri, echo=echo, logger=logger)
    db_config.init_db()

    # Create UnitOfWork
    uow = UnitOfWork.get_instance(db_config, logger)

    app = Flask(__name__)
    app.debug = debug
    app.use_reloader = use_reloader
    
    api_version = "1.0"

    # Create blueprint
    blueprint = Blueprint("api", __name__)
    api = Api(blueprint, version=api_version, title="API", description="A Simple API")

    # Add Namespaces
    address_version = "1"
    api.add_namespace(create_address_ns(api, uow, address_version, logger))
    email_version = "1"
    api.add_namespace(create_email_ns(api, uow, email_version, logger))
    person_version = "1"
    api.add_namespace(create_person_ns(api, uow, person_version, logger))

    # Register blueprint
    app.register_blueprint(blueprint)
    
    return app

