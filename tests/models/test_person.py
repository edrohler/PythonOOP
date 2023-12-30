import pytest
from core.models import Person
from sqlalchemy.orm import Session

@pytest.fixture
def mock_session(mocker):
    return mocker.MagicMock(spec=Session)

@pytest.fixture
def person():
    return Person("123456789", "John", "Doe", "M", 30)

def test_init(person):
    assert person.ssn == "123456789"
    assert person.firstname == "John"
    assert person.lastname == "Doe"
    assert person.gender == "M"
    assert person.age == 30

def test_repr(person):
    assert repr(person) == "(123456789) John Doe (M,30)"

def test_add_person_to_session(mock_session, person):
    mock_session.add.assert_not_called()
    mock_session.add(person)
    mock_session.add.assert_called_once_with(person)