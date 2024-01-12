from pytest_mock import mocker
from sqlalchemy import Column, String, text

from src.infrastructure.orm.entities.base_entity import BaseEntity
from src.infrastructure.orm.entities.email import Email
from src.infrastructure.orm.entities.person import Person

def test_init_engine(test_database_config):
    """ Test if `init_engine` correctly initializes the engine. """
    assert test_database_config.engine is not None
    assert test_database_config.Session is not None

def test_init_db(test_database_config):
    """ Test if `init_db` creates tables correctly. """
    with test_database_config.engine.connect() as connection:
        result = connection.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
        tables = [row[0] for row in result]
        assert "people" in tables  # Replace with actual table name

def test_get_session(test_session):
    """ Test if `get_session` returns a new session instance. """
    session1 = test_session
    session2 = test_session
    assert session1 is session2

def test_base_entity_listeners(test_database_config):
    """ Test if `before_insert_listener` and `before_update_listener` work correctly. """
    session = test_database_config.get_session()
    
    new_entity = Person(first_name="John", last_name="Doe")
    session.add(new_entity)
    session.commit()
    
    assert new_entity.created_at is not None
    assert new_entity.created_by == "system"
    
    new_entity.first_name = "Jane"
    session.commit()
    assert new_entity.updated_at is not None
    assert new_entity.updated_by == "system"
    
    