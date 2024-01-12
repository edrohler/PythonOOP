from flask_restx import Api
import pytest
from flask import url_for

import sys
sys.path.insert(0, "./src")

from src.api.endpoints.email import create_email_ns

def test_get_all_emails(client, mocker, mock_unit_of_work, mock_logger):
    # Arrange
    from src.api.app import app
    app.config["SERVER_NAME"] = "localhost:5000"
    
    mock_get_all_emails = mocker.patch("src.api.endpoints.email.EmailService.get_all_emails")
    mock_get_all_emails.return_value = [
        {"id": 1, "email_address": "mail1@nomail.com", "person_id": 1},
        {"id": 2, "email_address": "mail2@nomail.com", "person_id": 1},
    ]
    
    # Act
    with app.app_context():
        create_email_ns(Api(), "1.0", mock_unit_of_work, mock_logger)
        response = client.get(url_for("api.Email Endpoints_email_list"))
        
    # Assert
    assert response.status_code == 200
    assert len(response.json) == 2
    assert response.json[0]["id"] == 1
    assert response.json[0]["email_address"] == "mail1@nomail.com"
    assert response.json[0]["person_id"] == 1
    assert response.json[1]["id"] == 2
    assert response.json[1]["email_address"] == "mail2@nomail.com"
    assert response.json[1]["person_id"] == 1

def test_create_email(client, mocker, mock_unit_of_work, mock_logger):
    # Arrange
    from src.api.app import app
    app.config["SERVER_NAME"] = "localhost:5000"
    app.config["APPLICATION_ROOT"] = "/"
    app.config["PREFERRED_URL_SCHEME"] = "http"
    mock_create_email = mocker.patch("src.api.endpoints.email.EmailService.create_email")
    mock_create_email.return_value = {"message": "Email broken"}
    
    #Act
    with mock_create_email, app.app_context():
        create_email_ns(Api(), "1.0", mock_unit_of_work, mock_logger)
        response = client.post(url_for("api.Email Endpoints_email_list"),
                               json={"id": 0, "email_address": "mail1@nomail.com", "person_id": 1})
        
    # Assert
    assert response.status_code == 201
    assert response.json["message"] == "Email created"

def test_create_email_with_exception(mocker, mock_unit_of_work, mock_logger, client):
    # Arrange
    from src.api.app import app
    app.config["SERVER_NAME"] = "localhost:5000"
    app.config["APPLICATION_ROOT"] = "/"
    app.config["PREFERRED_URL_SCHEME"] = "http"
    mock_create_email = mocker.patch("src.api.endpoints.email.EmailService.create_email")
    mock_create_email.side_effect = Exception("An Error Occurred")
    
    #Act
    with mock_create_email, app.app_context():
        create_email_ns(Api(), "1.0", mock_unit_of_work, mock_logger)
        response = client.post(url_for("api.Email Endpoints_email_list"),
                               json={"id": 0, "email_address": "mail1@nomail.com", "person_id": 1})

    # Assert
    assert response.status_code == 400
    assert response.json["message"] == "An Error Occurred"

def test_update_email(client, mocker, mock_unit_of_work, mock_logger):
    # Arrange
    from src.api.app import app
    app.config["SERVER_NAME"] = "localhost:5000"
    app.config["APPLICATION_ROOT"] = "/"
    app.config["PREFERRED_URL_SCHEME"] = "http"
    mock_update_email = mocker.patch("src.api.endpoints.email.EmailService.update_email")
    mock_update_email.return_value = {"id": 1, "email_address": "mail1@nomail.com", "person_id": 1}
    
    #Act
    with mock_update_email, app.app_context():
        create_email_ns(Api(), "1.0", mock_unit_of_work, mock_logger)
        response = client.put(url_for("api.Email Endpoints_email_list", id=1),
                              json={"id": 1, "email_address": "mail1@nomail.com", "person_id": 1},
                              headers={"Content-Type": "application/json"})
        
    # Assert
    assert response.status_code == 200
    assert response.json["message"] == "Email updated"
    
def test_update_email_with_id_of_0(client, mocker, mock_unit_of_work, mock_logger):
    # Arrange
    from src.api.app import app
    app.config["SERVER_NAME"] = "localhost:5000"
    app.config["APPLICATION_ROOT"] = "/"
    app.config["PREFERRED_URL_SCHEME"] = "http"
    mock_update_email = mocker.patch("src.api.endpoints.email.EmailService.update_email")
    mock_update_email.side_effect = Exception("Id is required")
    
    #Act
    with app.app_context():
        create_email_ns(Api(), "1.0", mock_unit_of_work, mock_logger)
        response = client.put(url_for("api.Email Endpoints_email_list", id=0),
                              json={"id": 0, "email_address": "mail1@nomail.com", "person_id": 1},
                              headers={"Content-Type": "application/json"})
        
    # Assert
    assert response.status_code == 400
    assert response.json["message"] == "Error updating email"
    
def test_update_email_with_id_missing_from_payload(client, mocker, mock_unit_of_work, mock_logger):
    # Arrange
    from src.api.app import app
    app.config["SERVER_NAME"] = "localhost:5000"
    app.config["APPLICATION_ROOT"] = "/"
    app.config["PREFERRED_URL_SCHEME"] = "http"
    mock_update_email = mocker.patch("src.api.endpoints.email.EmailService.update_email")
    mock_update_email.side_effect = Exception("Id is required")
    
    #Act
    with app.app_context():
        create_email_ns(Api(), "1.0", mock_unit_of_work, mock_logger)
        response = client.put(url_for("api.Email Endpoints_email_list", id=1),
                              json={"email_address": "mail1@nomail.com", "person_id": 1},
                              headers={"Content-Type": "application/json"})
        
    # Assert
    assert response.status_code == 400
    assert response.json["message"] == "Id is required"
    
def test_get_email_by_id(client, mocker, mock_unit_of_work, mock_logger):
    #Arrange
    from src.api.app import app
    app.config["SERVER_NAME"] = "localhost:5000"
    app.config["APPLICATION_ROOT"] = "/"
    app.config["PREFERRED_URL_SCHEME"] = "http"
    mock_get_email_by_id = mocker.patch("src.api.endpoints.email.EmailService.get_email_by_id")
    mock_get_email_by_id.return_value = {"id": 1, "email_address": "mail1@nomail.com", "person_id": 1}
    
    # Act
    with app.app_context():
        create_email_ns(Api(), "1.0", mock_unit_of_work, mock_logger)
        response = client.get(url_for("api.Email Endpoints_email_resource", id=1))
        
    # Assert
    assert response.status_code == 200
    assert response.json["id"] == 1
    assert response.json["email_address"] == "mail1@nomail.com"
    assert response.json["person_id"] == 1
    
def test_get_email_by_id_with_not_found(client, mocker, mock_unit_of_work, mock_logger):
    #Arrange
    from src.api.app import app
    app.config["SERVER_NAME"] = "localhost:5000"
    
    mock_get_email_by_id = mocker.patch("src.api.endpoints.email.EmailService.get_email_by_id")
    mock_get_email_by_id.return_value = None
    
    # Act
    with app.app_context():
        create_email_ns(Api(), "1.0", mock_unit_of_work, mock_logger)
        response = client.get(url_for("api.Email Endpoints_email_resource", id=1))
        
    # Assert
    assert response.status_code == 404
    assert response.json["message"] == "Email not found"
    
def test_delete_email(client, mocker, mock_unit_of_work, mock_logger):
    #Arrange
    from src.api.app import app
    app.config["SERVER_NAME"] = "localhost:5000"
    mock_delete_email = mocker.patch("src.api.endpoints.email.EmailService.delete_email")
    mock_delete_email.return_value = {"message": "Email deleted"}
    
    #Act
    with app.app_context():
        create_email_ns(Api(), "1.0", mock_unit_of_work, mock_logger)
        response = client.delete(url_for("api.Email Endpoints_email_resource", id=1))
        
    assert response.status_code == 200
    assert response.json["message"] == "Email with id: 1 deleted"
    
def test_delete_email_with_exection(client, mocker, mock_unit_of_work, mock_logger):
    #Arrange
    from src.api.app import app
    app.config["SERVER_NAME"] = "localhost:5000"
    mock_delete_email = mocker.patch("src.api.endpoints.email.EmailService.delete_email")
    mock_delete_email.side_effect = Exception("An Error Occurred")
    
    #Act
    with app.app_context():
        create_email_ns(Api(), "1.0", mock_unit_of_work, mock_logger)
        response = client.delete(url_for("api.Email Endpoints_email_resource", id=1))
        
    assert response.status_code == 400
    assert response.json["message"] == "Error deleting email"