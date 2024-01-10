from src.core.services.person_service import PersonService
from src.core.domain.models.person import Person


def test_get_person_by_id(mock_unit_of_work, mocker):
    # Arrange
    person_service = PersonService(mock_unit_of_work)
    person_id = 1
    mock_get_by_id = mocker.patch.object(mock_unit_of_work.person_repository, 'get_by_id')
    mock_get_by_id.return_value = Person(id=1, first_name='John', last_name='Doe', gender='Male', age=30)

    # Act
    result = person_service.get_person_by_id(person_id)

    # Assert
    assert isinstance(result, Person)
    assert result.id == person_id

def test_get_all_people(mock_unit_of_work, mocker):
    # Arrange
    person_service = PersonService(mock_unit_of_work)
    mock_get_all = mocker.patch.object(mock_unit_of_work.person_repository, 'get_all')
    mock_get_all.return_value = [Person(id=1, first_name='John', last_name='Doe', gender='Male', age=30)]

    # Act
    result = person_service.get_all_people()

    # Assert
    assert isinstance(result, list)
    assert all(isinstance(person, Person) for person in result)

def test_create_person(mock_unit_of_work, mocker):
    # Arrange
    person_service = PersonService(mock_unit_of_work)
    mocker_commit = mocker.patch.object(mock_unit_of_work, 'commit')
    person = Person(id=1, first_name='John', last_name='Doe', gender='Male', age=30)
    mocker_add = mocker.patch.object(mock_unit_of_work.person_repository, 'add')
    mocker_add.return_value = None

    # Act
    person_service.create_person(person)

    # Assert
    mock_unit_of_work.person_repository.add.assert_called_once()

def test_update_person(mock_unit_of_work, mocker):
    # Arrange
    person_service = PersonService(mock_unit_of_work)
    person = Person(id=1, first_name='John', last_name='Doe', gender='Male', age=30)
    mocker_update = mocker.patch.object(mock_unit_of_work.person_repository, 'update')
    mocker_update.return_value = None

    # Act
    person_service.update_person(person)

    # Assert
    mock_unit_of_work.person_repository.update.assert_called_once()

def test_delete_person(mock_unit_of_work, mocker):
    # Arrange
    person_service = PersonService(mock_unit_of_work)
    mocker_commit = mocker.patch.object(mock_unit_of_work, 'commit')
    person_id = 1
    mock_delete = mocker.patch.object(mock_unit_of_work.person_repository, 'delete')
    mock_delete.return_value = None

    # Act
    person_service.delete_person(person_id)

    # Assert
    mock_unit_of_work.person_repository.delete.assert_called_once()
