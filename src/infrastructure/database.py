from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from src.infrastructure.orm.entities import BaseEntity

class DatabaseConfig:
    def __init__(self, database_uri='sqlite:///database.db', echo=True):
        self.database_uri = database_uri
        self.echo = echo
        self.engine = None
        self.Session = None

    def init_engine(self):
        self.engine = create_engine(self.database_uri, echo=self.echo)
        self.Session = sessionmaker(bind=self.engine)

    def init_db(self):
        """ Initialize the database (create tables based on models) """
        if not self.engine:
            self.init_engine()
        BaseEntity.metadata.create_all(self.engine)

    def get_session(self):
        """ Returns a new session instance from the session factory """
        if not self.Session:
            self.init_engine()
        return self.Session()

# Default configuration
default_config = DatabaseConfig()

def init_db():
    default_config.init_db()

def get_session():
    return default_config.get_session()
