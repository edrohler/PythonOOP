import logging
from flask import Flask
from flask_restx import Api

from core.services.logging_service import LoggingService
from infrastructure.database import get_session
from infrastructure.database import DatabaseConfig

# from .endpoints.person import ns as person_ns
from .endpoints.address import ns as address_ns
# from .endpoints.email import ns as email_ns

app = Flask(__name__)

# Configure logging
logger = LoggingService(logger_name='api', log_level='DEBUG', handler=logging.FileHandler('api.log'))

# Configure database
db_config = DatabaseConfig(database_uri="sqlite:///database.db", echo=True, logger=logger)
db_config.init_db()
session = get_session(db_config)

api = Api()
api.init_app(app)
api.add_namespace(address_ns)
# api.add_namespace(email_ns)
# api.add_namespace(person_ns)
