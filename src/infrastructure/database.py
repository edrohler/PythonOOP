from datetime import datetime
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, class_mapper

from src.core.services.logging_service import LoggingService
from .orm.entities import BaseEntity

class DatabaseConfig:
    _instance = None  # Class attribute to hold the singleton instance

    @classmethod
    def get_instance(cls, database_uri="sqlite:///database.db", echo=False, logger: LoggingService = None):
        """ Class method to get the singleton instance of the class. """
        if cls._instance is None:
            cls._instance = cls(database_uri, echo, logger)
        return cls._instance

    def __init__(self, database_uri, echo, logger):
        """ Constructor is made private to prevent direct instantiation. """
        self.database_uri = database_uri
        self.echo = echo
        self.engine = None
        self.Session = None
        self.logger = logger

    def init_engine(self):
        self.engine = create_engine(self.database_uri, echo=self.echo)
        self.Session = sessionmaker(bind=self.engine)
        self.logger.log_info(f"Initialized database engine with URI {self.database_uri}")

    def init_db(self):
        """ Initialize the database (create tables based on models) """
        if not self.engine:
            self.init_engine()
        BaseEntity.metadata.create_all(self.engine)
        self.logger.log_info("Initialized database")

    def get_session(self):
        """ Returns a new session instance from the session factory """
        if not self.Session:
            self.logger.log_info("No session available. Initializing")
            self.init_engine()
        self.register_listeners()
        self.logger.log_info("Returning session")
        return self.Session()
        
    def register_listeners(self):
        """ Registers event listeners for all entities """
        self.logger.log_info("Registering event listeners")
        for cls in BaseEntity.__subclasses__():
                mapped_class = class_mapper(cls)
                event.listen(mapped_class, 'before_insert', self.before_insert_listener)
                self.logger.log_info(f"Registered before_insert listener for {cls.__name__}")
                event.listen(mapped_class, 'before_update', self.before_update_listener)
                self.logger.log_info(f"Registered before_update listener for {cls.__name__}")

    @staticmethod
    def before_insert_listener(mapper, connection, target):
        target.created_at = datetime.utcnow()
        target.created_by = "system" # TODO: Get user from session
    @staticmethod
    def before_update_listener(mapper, connection, target):
        target.updated_at = datetime.utcnow()
        target.updated_by = "system" # TODO: Get user from session
    