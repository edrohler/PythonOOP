from flask_restx import Api
import pytest
from flask import url_for

import sys
sys.path.insert(0, "./src")

from src.api.endpoints.address import create_address_ns

def test_get_all_addresses(client, mocker, mock_unit_of_work, mock_logger):
    # Arrange
    from src.api.app import app
    app.config["SERVER_NAME"] = "localhost:5000"
    
    mock_get_all_addresses = mocker.patch("src.api.endpoints.address.AddressService.get_all_addresses")
    mock_get_all_addresses.return_value = [
        {"id": 1, "address_line_1": "123 Main St", "city": "Anytown", "state": "CA", "zip_code": "12345"},
        {"id": 2, "address_line_1": "456 Main St", "city": "Anytown", "state": "CA", "zip_code": "12345"}
    ]
    
    # Act
    with app.app_context():
        create_address_ns(Api(), "1.0", mock_unit_of_work, mock_logger)
        response = client.get(url_for("api.Address Endpoints_address_list"))

    # Assert
    assert response.status_code == 200
    assert len(response.json) == 2
    assert response.json[0]["id"] == 1
    assert response.json[0]["address_line_1"] == "123 Main St"
    assert response.json[0]["city"] == "Anytown"
    assert response.json[0]["state"] == "CA"
    assert response.json[0]["zip_code"] == "12345"
    assert response.json[1]["id"] == 2
    assert response.json[1]["address_line_1"] == "456 Main St"
    assert response.json[1]["city"] == "Anytown"
    assert response.json[1]["state"] == "CA"
    assert response.json[1]["zip_code"] == "12345"

def test_create_address(client, mocker, mock_unit_of_work, mock_logger):
    # Arrange
    from src.api.app import app
    app.config["SERVER_NAME"] = "localhost:5000"
    app.config["APPLICATION_ROOT"] = "/"
    app.config["PREFERRED_URL_SCHEME"] = "http"
    mock_create_address = mocker.patch("src.api.endpoints.address.AddressService.create_address")
    mock_create_address.return_value = {"message": "Address broken"}
    
    #Act
    with mock_create_address, app.app_context():
        create_address_ns(Api(), "1.0", mock_unit_of_work, mock_logger)
        response = client.post(url_for("api.Address Endpoints_address_list"), json={"id": 0, "address_line_1": "123 Main St", "address_line_2": "", "city": "Anytown", "state": "CA", "zip_code": "12345", "person_id": 1})
        
    # Assert
    assert response.status_code == 201
    assert response.json["message"] == "Address created"
    
def test_create_address_with_exception(mocker, mock_unit_of_work, mock_logger, client):
    # Arrange
    from src.api.app import app
    app.config["SERVER_NAME"] = "localhost:5000"
    app.config["APPLICATION_ROOT"] = "/"
    app.config["PREFERRED_URL_SCHEME"] = "http"
    mock_create_address = mocker.patch("src.api.endpoints.address.AddressService.create_address")
    mock_create_address.side_effect = Exception("An Error Occurred")
    
    # Act
    with mock_create_address, app.app_context():
        create_address_ns(Api(), "1.0", mock_unit_of_work, mock_logger)
        response = client.post(url_for("api.Address Endpoints_address_list"), json={"id": 0, "address_line_1": "123 Main St", "address_line_2": "", "city": "Anytown", "state": "CA", "zip_code": "12345", "person_id": 1})
        
    # Assert
    assert response.status_code == 400
    assert response.json["message"] == "An Error Occurred"
    
def test_update_address(client, mocker, mock_unit_of_work, mock_logger):
    #Arrange
    from src.api.app import app
    app.config["SERVER_NAME"] = "localhost:5000"
    app.config["APPLICATION_ROOT"] = "/"
    app.config["PREFERRED_URL_SCHEME"] = "http"
    mock_update_address = mocker.patch("src.api.endpoints.address.AddressService.update_address")
    mock_update_address.return_value = {"id": 1, "address_line_1": "123 Main St", "address_line_2": "", "city": "Anytown", "state": "CA", "zip_code": "12345", "person_id": 1}

    #Act
    with app.app_context():
        create_address_ns(Api(), "1.0", mock_unit_of_work, mock_logger)
        response = client.put(url_for("api.Address Endpoints_address_list"),
                              json={"id": 1, "address_line_1": "123 Main St", "address_line_2": "", "city": "Anytown", "state": "CA", "zip_code": "12345", "person_id": 1},
                              headers={"Content-Type": "application/json"})
    
    #Assert
    assert response.status_code == 200
    assert response.json["message"] == "Address updated"

def test_update_address_with_id_of_0(mocker, mock_unit_of_work, mock_logger, client):
    #Arrange
    from src.api.app import app
    app.config["SERVER_NAME"] = "localhost:5000"
    app.config["APPLICATION_ROOT"] = "/"
    app.config["PREFERRED_URL_SCHEME"] = "http"
    mock_update_address = mocker.patch("src.api.endpoints.address.AddressService.update_address")
    mock_update_address.side_effect = Exception("Id is required")

    #Act
    with app.app_context():
        create_address_ns(Api(), "1.0", mock_unit_of_work, mock_logger)
        response = client.put(url_for("api.Address Endpoints_address_list"),
                              json={"id": 0, "address_line_1": "123 Main St", "address_line_2": "", "city": "Anytown", "state": "CA", "zip_code": "12345", "person_id": 1},
                              headers={"Content-Type": "application/json"})
    
    #Assert
    assert response.status_code == 400
    assert response.json["message"] == "Error updating address"
    
def test_update_address_with_id_missing_from_payload(mocker, mock_unit_of_work, mock_logger, client):
    #Arrange
    from src.api.app import app
    app.config["SERVER_NAME"] = "localhost:5000"
    app.config["APPLICATION_ROOT"] = "/"
    app.config["PREFERRED_URL_SCHEME"] = "http"
    mock_update_address = mocker.patch("src.api.endpoints.address.AddressService.update_address")
    mock_update_address.side_effect = Exception("Id is required")
    
    #Act
    with app.app_context():
        create_address_ns(Api(), "1.0", mock_unit_of_work, mock_logger)
        response = client.put(url_for("api.Address Endpoints_address_list"),
                              json={"address_line_1": "123 Main St", "address_line_2": "", "city": "Anytown", "state": "CA", "zip_code": "12345", "person_id": 1},
                              headers={"Content-Type": "application/json"})
    
    #Assert
    assert response.status_code == 400
    assert response.json["message"] == "Id is required"
    
def test_get_address_by_id(client, mocker, mock_unit_of_work, mock_logger):
    #Arrange
    from src.api.app import app
    app.config["SERVER_NAME"] = "localhost:5000"
    app.config["APPLICATION_ROOT"] = "/"
    app.config["PREFERRED_URL_SCHEME"] = "http"
    mock_get_address_by_id = mocker.patch("src.api.endpoints.address.AddressService.get_address_by_id")
    mock_get_address_by_id.return_value = {"id": 1, "address_line_1": "123 Main St", "address_line_2": "", "city": "Anytown", "state": "CA", "zip_code": "12345", "person_id": 1}
    
    #Act
    with app.app_context():
        create_address_ns(Api(), "1.0", mock_unit_of_work, mock_logger)
        response = client.get(url_for("api.Address Endpoints_address_resource", id=1))
        
    #Assert
    assert response.status_code == 200
    assert response.json["id"] == 1
    assert response.json["address_line_1"] == "123 Main St"
    assert response.json["address_line_2"] == ""
    assert response.json["city"] == "Anytown"
    assert response.json["state"] == "CA"
    assert response.json["zip_code"] == "12345"
    assert response.json["person_id"] == 1
    
def test_get_address_by_id_with_not_found(mocker, mock_unit_of_work, mock_logger, client):
    #Arrange
    from src.api.app import app
    app.config["SERVER_NAME"] = "localhost:5000"
    mock_get_address_by_id = mocker.patch("src.api.endpoints.address.AddressService.get_address_by_id")
    mock_get_address_by_id.return_value = None
    
    #Act
    with app.app_context():
        create_address_ns(Api(), "1.0", mock_unit_of_work, mock_logger)
        response = client.get(url_for("api.Address Endpoints_address_resource", id=1))
        
    #Assert
    assert response.status_code == 404
    assert response.json["message"] == "Address not found"
    
def test_delete_address(client, mocker, mock_unit_of_work, mock_logger):
    #Arrange
    from src.api.app import app
    app.config["SERVER_NAME"] = "localhost:5000"
    app.config["APPLICATION_ROOT"] = "/"
    app.config["PREFERRED_URL_SCHEME"] = "http"
    mock_delete_address = mocker.patch("src.api.endpoints.address.AddressService.delete_address")
    mock_delete_address.return_value = {"message": "Address deleted"}
    
    #Act
    with app.app_context():
        create_address_ns(Api(), "1.0", mock_unit_of_work, mock_logger)
        response = client.delete(url_for("api.Address Endpoints_address_resource", id=1))
        
    #Assert
    assert response.status_code == 200
    assert response.json["message"] == "Address with id: 1 deleted"
    
def test_delete_address_with_exception(mocker, mock_unit_of_work, mock_logger, client):
    #Arrange
    from src.api.app import app
    app.config["SERVER_NAME"] = "localhost:5000"
    mock_delete_address = mocker.patch("src.api.endpoints.address.AddressService.delete_address")
    mock_delete_address.side_effect = Exception("Test exception")
    
    #Act
    with app.app_context():
        create_address_ns(Api(), "1.0", mock_unit_of_work, mock_logger)
        response = client.delete(url_for("api.Address Endpoints_address_resource", id=1))
        
    #Assert
    assert response.status_code == 400
    assert response.json["message"] == "Error deleting address"