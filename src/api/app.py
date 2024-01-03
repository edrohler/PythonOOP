import logging
from flask import Flask
from flask_restx import Api

from core.services.logging_service import LoggingService
from infrastructure.database import get_session
from infrastructure.database import DatabaseConfig
from infrastructure.unit_of_work import UnitOfWork


# from .endpoints.person import ns as person_ns
from .endpoints.address import create_address_blueprint
# from .endpoints.email import ns as email_ns

# Configure logging
logger = LoggingService(logger_name="api", log_level="DEBUG", handler=logging.FileHandler("logs/.log"))

# Configure database
db_config = DatabaseConfig.get_instance(database_uri="sqlite:///database.db", echo=True, logger=logger)
db_config.init_db()

# Create UnitOfWork
uow = UnitOfWork.get_instance(db_config, logger)

app = Flask(__name__)


address_bp = create_address_blueprint(uow, version="v1")
app.register_blueprint(address_bp)