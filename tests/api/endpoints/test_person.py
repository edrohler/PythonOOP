from flask_restx import Api
import pytest
from flask import url_for

import sys
sys.path.insert(0, "./src")

from src.api.endpoints.person import create_person_ns

def test_get_all_people(client, mocker, mock_unit_of_work, mock_logger):
    # Arrange
    from src.api.app import app
    app.config["SERVER_NAME"] = "localhost:5000"
    
    mock_get_all_people = mocker.patch("src.api.endpoints.person.PersonService.get_all_people")
    mock_get_all_people.return_value = [
        {"id": 1, "first_name": "John", "last_name": "Doe", "gender": "Male", "age": 30},
        {"id": 2, "first_name": "Jane", "last_name": "Doe", "gender": "Female", "age": 28}
    ]
    
    # Act
    with app.app_context():
        create_person_ns(Api(), "1.0", mock_unit_of_work, mock_logger)
        response = client.get(url_for("api.Person Endpoints_people_list"))

    # Assert
    assert response.status_code == 200
    assert len(response.json) == 2
    assert response.json[0]["id"] == 1
    assert response.json[0]["first_name"] == "John"
    assert response.json[0]["last_name"] == "Doe"
    assert response.json[0]["gender"] == "Male"
    assert response.json[0]["age"] == 30
    assert response.json[1]["id"] == 2
    assert response.json[1]["first_name"] == "Jane"
    assert response.json[1]["last_name"] == "Doe"
    assert response.json[1]["gender"] == "Female"
    assert response.json[1]["age"] == 28

def test_create_person(client, mocker, mock_unit_of_work, mock_logger):
    # Arrange
    from src.api.app import app
    app.config["SERVER_NAME"] = "localhost:5000"
    app.config["APPLICATION_ROOT"] = "/"
    app.config["PREFERRED_URL_SCHEME"] = "http"
    mock_create_person = mocker.patch("src.api.endpoints.person.PersonService.create_person")
    mock_create_person.return_value = {"message": "Person broken"}

    # Act
    with mock_create_person, app.app_context():
        create_person_ns(Api(), "1.0", mock_unit_of_work, mock_logger)
        response = client.post(url_for("api.Person Endpoints_people_list"), json={"id": 0, "first_name": "John", "last_name": "Doe", "gender": "M", "age": 30})

    # Assert
    assert response.status_code == 201
    assert response.json["message"] == "Person created"
    
def test_create_person_with_exception(mocker, mock_unit_of_work, mock_logger, client):
    # Arrange
    from src.api.app import app
    app.config["SERVER_NAME"] = "localhost:5000"
    app.config["APPLICATION_ROOT"] = "/"
    app.config["PREFERRED_URL_SCHEME"] = "http"
    mock_create_person = mocker.patch("src.api.endpoints.person.PersonService.create_person")
    mock_create_person.side_effect = Exception("Test excpetion")
    
    with app.app_context():
        create_person_ns(Api(), "1.0", mock_unit_of_work, mock_logger)
        response = client.post(url_for("api.Person Endpoints_people_list"), json={"id": 0, "first_name": "John", "last_name": "Doe", "gender": "M", "age": 30})
    
    assert response.status_code == 400
    assert response.json["message"] == "An Error Occurred"

def test_update_person(client, mocker, mock_unit_of_work, mock_logger):
    # Arrange
    from src.api.app import app
    app.config["SERVER_NAME"] = "localhost:5000"
    app.config["APPLICATION_ROOT"] = "/"
    app.config["PREFERRED_URL_SCHEME"] = "http"    
    mock_update_person = mocker.patch("src.api.endpoints.person.PersonService.update_person")
    mock_update_person.return_value = {"id": 1, "first_name": "John", "last_name": "Doe", "gender": "Male", "age": 31}

    # Act
    with app.app_context():
        create_person_ns(Api(), "1.0", mock_unit_of_work, mock_logger)
        response = client.put(url_for("api.Person Endpoints_people_list"), 
                              json={"id": 1, "first_name": "John", "last_name": "Doe", "gender": "M", "age": 30},
                              headers={"Content-Type": "application/json"})

    # Assert
    assert response.status_code == 200
    assert response.json["message"] == "Person updated"
    
def test_update_person_with_id_of_0(mocker, mock_unit_of_work, mock_logger, client):
    # Arrange
    from src.api.app import app
    app.config["SERVER_NAME"] = "localhost:5000"
    app.config["APPLICATION_ROOT"] = "/"
    app.config["PREFERRED_URL_SCHEME"] = "http"    
    mock_update_person = mocker.patch("src.api.endpoints.person.PersonService.update_person")
    mock_update_person.side_effect = Exception("Id is required")
    
    
    with app.app_context():
        create_person_ns(Api(), "1.0", mock_unit_of_work, mock_logger)
        response = client.put(url_for("api.Person Endpoints_people_list"),
                                      json={"id": 0, "first_name": "John", "last_name": "Doe", "gender": "M", "age": 31},
                                      headers={"Content-Type": "application/json"})
        
    assert response.status_code == 400
    assert response.json["message"] == "Error updating person"

def test_update_person_with_id_missing_from_payload(mocker, mock_unit_of_work, mock_logger, client):    
    # Arrange
    from src.api.app import app
    app.config["SERVER_NAME"] = "localhost:5000"
    app.config["APPLICATION_ROOT"] = "/"
    app.config["PREFERRED_URL_SCHEME"] = "http"    
    mock_update_person = mocker.patch("src.api.endpoints.person.PersonService.update_person")
    mock_update_person.side_effect = Exception("Id is required")
    
    
    with app.app_context():
        create_person_ns(Api(), "1.0", mock_unit_of_work, mock_logger)
        response = client.put(url_for("api.Person Endpoints_people_list"),
                                      json={"first_name": "John", "last_name": "Doe", "gender": "M", "age": 31},
                                      headers={"Content-Type": "application/json"})
        
    assert response.status_code == 400
    assert response.json["message"] == "Id is required"    
    

def test_get_person_by_id(client, mocker, mock_unit_of_work, mock_logger):
    # Arrange
    from src.api.app import app
    app.config["SERVER_NAME"] = "localhost:5000"
    app.config["APPLICATION_ROOT"] = "/"
    app.config["PREFERRED_URL_SCHEME"] = "http"        
    mock_get_person_by_id = mocker.patch("src.api.endpoints.person.PersonService.get_person_by_id")
    mock_get_person_by_id.return_value = {"id": 1, "first_name": "John", "last_name": "Doe", "gender": "Male", "age": 30}

    # Act
    with app.app_context():
        create_person_ns(Api(), "1.0", mock_unit_of_work, mock_logger)
        response = client.get(url_for("api.Person Endpoints_people_resource", id=1))

    # Assert
    assert response.status_code == 200
    assert response.json["id"] == 1
    ...
    
def test_get_person_by_id_with_exception(mocker, mock_unit_of_work, mock_logger, client):
    #Arrange
    from src.api.app import app
    app.config["SERVER_NAME"] = "localhost:5000"
    app.config["APPLICATION_ROOT"] = "/"
    app.config["PREFERRED_URL_SCHEME"] = "http"
    mock_get_person_by_id = mocker.patch("src.api.endpoints.person.PersonService.get_person_by_id")
    mock_get_person_by_id.return_value = {"message": "Person not found"}
    
    #Act
    with app.app_context():
        create_person_ns(Api(), "1.0", mock_unit_of_work, mock_logger)
        response = client.get(url_for("api.Person Endpoints_people_resource", id=999))
        
    #Assert
    assert response.status_code == 200
    assert response.json["message"] == "Person not found"

def test_delete_person(client, mocker, mock_unit_of_work, mock_logger):
    # Arrange
    from src.api.app import app
    app.config["SERVER_NAME"] = "localhost:5000"
    app.config["APPLICATION_ROOT"] = "/"
    app.config["PREFERRED_URL_SCHEME"] = "http"        
    mock_delete_person = mocker.patch("src.api.endpoints.person.PersonService.delete_person")
    mock_delete_person.return_value = {"message": "Person with id: 1 deleted"}

    # Act
    with app.app_context():
        create_person_ns(Api(), "1.0", mock_unit_of_work, mock_logger)
        response = client.delete(url_for("api.Person Endpoints_people_resource", id=1))

    # Assert
    assert response.status_code == 200
    assert response.json["message"] == "Person with id: 1 deleted"   
    
def test_delete_person_with_exception(mocker, mock_unit_of_work, mock_logger, client):
    # Arrange
    from src.api.app import app
    app.config["SERVER_NAME"] = "localhost:5000"
    app.config["APPLICATION_ROOT"] = "/"
    app.config["PREFERRED_URL_SCHEME"] = "http"        
    mock_delete_person = mocker.patch("src.api.endpoints.person.PersonService.delete_person")
    mock_delete_person.side_effect = Exception("Test exception")

    # Act
    with app.app_context():
        create_person_ns(Api(), "1.0", mock_unit_of_work, mock_logger)
        response = client.delete(url_for("api.Person Endpoints_people_resource", id=1))

    # Assert
    assert response.status_code == 400
    assert response.json["message"] == "Error deleting person" 