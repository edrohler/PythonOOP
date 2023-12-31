from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from infrastructure.entities.base_entity import BaseEntity, Person, Address, Email

# Database URI (Change according to your database)
DATABASE_URI = 'sqlite:///mylibrary.db'  # Example for SQLite
# For other databases, the URI format will differ. For example,
# PostgreSQL: 'postgresql://user:password@localhost/mylibrary'


# Create the SQLAlchemy engine with the database URI
engine = create_engine(DATABASE_URI, echo=True)  # Set echo to False in production

# Create a session factory bound to this engine
Session = sessionmaker(bind=engine)

def init_db():
    """ Initialize the database (create tables based on models) """
    BaseEntity.metadata.create_all(engine)

def get_session():
    """ Returns a new session instance from the session factory """
    return Session()