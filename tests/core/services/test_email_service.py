from src.core.services.email_service import EmailService as EmailService
from src.core.domain.models.email import Email as Email

def test_get_email_by_id(mock_unit_of_work, mocker):
    # Arrange
    email_service = EmailService(mock_unit_of_work)
    email_id = 1
    mock_get_by_id = mocker.patch.object(mock_unit_of_work.email_repository, "get_by_id")
    mock_get_by_id.return_value = Email(id=1, email_address="test1@nomail.com", person_id=1)
    
    # Act
    result = email_service.get_email_by_id(email_id)
    
    # Assert
    assert isinstance(result, Email)
    assert result.id == email_id
    
def test_get_all_emails(mock_unit_of_work, mocker):
    # Arrange
    email_service = EmailService(mock_unit_of_work)
    mock_get_all = mocker.patch.object(mock_unit_of_work.email_repository, "get_all")
    mock_get_all.return_value = [Email(id=1, email_address="test1@nomail.com", person_id=1)]
    
    # Act
    result = email_service.get_all_emails()
    
    # Assert
    assert isinstance(result, list)
    assert all(isinstance(email, Email) for email in result)
def test_create_address(mock_unit_of_work, mocker):
    # Arrange
    email_service = EmailService(mock_unit_of_work)
    mocker_commit = mocker.patch.object(mock_unit_of_work, "commit")
    email = Email(id=1, email_address="test1@nomail.com", person_id=1)
    mocker_add = mocker.patch.object(mock_unit_of_work.email_repository, "add")
    mocker_add.return_value = None
    
    # Act
    email_service.create_email(email)
    
    # Assert
    mock_unit_of_work.email_repository.add.assert_called_once()
    mocker_commit.assert_called_once()
    
def test_update_email(mock_unit_of_work, mocker):
    # Arrange
    email_service = EmailService(mock_unit_of_work)
    email = Email(id=1, email_address="test1@nomail.com", person_id=1)
    mocker_update = mocker.patch.object(mock_unit_of_work.email_repository, "update")
    mocker_update.return_value = None
    
    # Act
    email_service.update_email(email)
    
    # Assert
    mock_unit_of_work.email_repository.update.assert_called_once()
    
def test_delete_email(mock_unit_of_work, mocker):
    # Arrange
    email_service = EmailService(mock_unit_of_work)
    email = Email(id=1, email_address="test1@nomail.com", person_id=1)
    mocker_delete = mocker.patch.object(mock_unit_of_work.email_repository, "delete")
    mocker_delete.return_value = None
    mocker_commit = mocker.patch.object(mock_unit_of_work, "commit")
    
    # Act
    email_service.delete_email(email.id)
    
    # Assert
    mock_unit_of_work.email_repository.delete.assert_called_once()
    mocker_commit.assert_called_once()