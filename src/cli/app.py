import logging

from src.core.services.logging_service import LoggingService
from src.infrastructure.database import DatabaseConfig
from src.infrastructure.unit_of_work import UnitOfWork

# Configure logging
logger = LoggingService(logger_name="cli", log_level="DEBUG", handler=logging.FileHandler("logs/.log"))

# Configure database
db_config = DatabaseConfig.get_instance(database_uri="sqlite:///database.db", echo=True, logger=logger)
db_config.init_db()

# Create Unit of Work
uow = UnitOfWork.get_instance(db_config, logger)