from flask_restx import Api, fields as restx_fields
from flask_restx.model import Model as RestxModel
from marshmallow import Schema, fields as ma_fields
import pytest
from src.api.utils import schema_to_api_model

class MyNestedSchema(Schema):
    name = ma_fields.String()

class MySchema(Schema):
    name = ma_fields.String()
    age = ma_fields.Integer()
    height = ma_fields.Float()
    is_active = ma_fields.Boolean()
    nested = ma_fields.Nested(MyNestedSchema)

def test_schema_to_api_model():
    api = Api()
    model = schema_to_api_model(MySchema(), api)

    assert isinstance(model, RestxModel)
    assert 'name' in model
    assert isinstance(model['name'], restx_fields.String)
    assert 'age' in model
    assert isinstance(model['age'], restx_fields.Integer)
    assert 'height' in model
    assert isinstance(model['height'], restx_fields.Float)
    assert 'is_active' in model
    assert isinstance(model['is_active'], restx_fields.Boolean)
    assert 'nested' in model
    assert isinstance(model['nested'], restx_fields.Nested)
    
def test_schema_to_api_model_raise_error(mocker):
    mocker.patch.object(ma_fields, "Nested", side_effect=Exception("Test exception"))
    with pytest.raises(Exception):
        schema_to_api_model(MySchema(), Api())
        
class MyNotImplementedTestSchema(Schema):
    test_field = ma_fields.DateTime()

def test_schema_to_api_model_not_implemented_error():
    api = Api()
    with pytest.raises(NotImplementedError):
        schema_to_api_model(MyNotImplementedTestSchema(), api)