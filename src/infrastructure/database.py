from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.core.services.logging_service import LoggingService
from .orm.entities import BaseEntity

class DatabaseConfig:
    _instance = None  # Class attribute to hold the singleton instance

    @classmethod
    def get_instance(cls, database_uri='sqlite:///database.db', echo=False, logger: LoggingService = None):
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
        self.logger.log_info(f'Initialized database engine with URI {self.database_uri}')

    def init_db(self):
        """ Initialize the database (create tables based on models) """
        if not self.engine:
            self.init_engine()
        BaseEntity.metadata.create_all(self.engine)
        self.logger.log_info('Initialized database')

    def get_session(self):
        """ Returns a new session instance from the session factory """
        if not self.Session:
            self.init_engine()
        self.logger.log_info('Created new session')
        return self.Session()

def init_db(config):
    config.init_db()

def get_session(config):
    return config.get_session()
