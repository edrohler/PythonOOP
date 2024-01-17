import logging

from src.core.services.logging_service import LoggingService
from src.infrastructure.database import DatabaseConfig
from src.infrastructure.unit_of_work import UnitOfWork

def app(debug=False):
    
    print()
    
    _log_level = "DEBUG" if debug else "INFO"
    _echo = True if debug else False
    
    # Configure logging
    logger = LoggingService(logger_name="cli", log_level=_log_level, handler=logging.FileHandler("logs/.log"))

    # Configure database
    db_config = DatabaseConfig.get_instance(database_uri="sqlite:///database.db", echo=_echo, logger=logger)
    db_config.init_db()

    # Create Unit of Work
    uow = UnitOfWork.get_instance(db_config, logger)
    
    run_cli(uow, logger)

            
def run_cli(uow, logger):
    while True:
        print("Welcome to the CLI!")

        choice = input("What would you like to do? (1) Enter the Person Context, (2) Enter the Address Context, (3) Enter the Email Context, (4) Exit: ")
        
        if choice == "1":
            handle_person_context(uow, logger)
        elif choice == "2":
            handle_address_context(uow, logger)
        elif choice == "3":
            handle_email_context(uow, logger)
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please choose between 1 and 4.")
            
def handle_person_context(uow, logger):
    # Implement person context functionality
    print("Person Context - Not implemented yet.")

def handle_address_context(uow, logger):
    # Implement address context functionality
    print("Address Context - Not implemented yet.")

def handle_email_context(uow, logger):
    # Implement email context functionality
    print("Email Context - Not implemented yet.")