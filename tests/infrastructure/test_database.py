from sqlalchemy import text

def test_init_engine(test_database_config):
    """ Test if `init_engine` correctly initializes the engine. """
    # Assuming init_engine is called within init_db
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