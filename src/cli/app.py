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
    
    while True:
        print("Welcome to the CLI!")

        choice = input("What would you like to do? (1) Enter the Person Context, (2) Enter the Address Context, (3) Enter the Email Context, (4) Exit: ")
        
        if choice == "1":
            # from src.cli.person_cli import PersonCLI
            # PersonCLI(uow, logger).run()
            print("Not implemented yet.")
        elif choice == "2":
            # from src.cli.address_cli import AddressCLI
            # AddressCLI(uow, logger).run()
            print("Not implemented yet.")
        elif choice == "3":
            # from src.cli.email_cli import EmailCLI
            # EmailCLI(uow, logger).run()
            print("Not implemented yet.")
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please choose between 1 and 4.")