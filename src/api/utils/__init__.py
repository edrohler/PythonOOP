from flask_restx import Api, Model, fields as restx_fields
from marshmallow import Schema, fields as ma_fields

def schema_to_model(schema: Schema, api: Api):
    model_fields = {}
    for field_name, field in schema._declared_fields.items():
        if isinstance(field, ma_fields.String):
            model_fields[field_name] = restx_fields.String()
        elif isinstance(field, ma_fields.Integer):
            model_fields[field_name] = restx_fields.Integer()
        elif isinstance(field, ma_fields.Float):
            model_fields[field_name] = restx_fields.Float()
        elif isinstance(field, ma_fields.Boolean):
            model_fields[field_name] = restx_fields.Boolean()
        elif isinstance(field, ma_fields.Nested):
            model_fields[field_name] = restx_fields.Nested(schema_to_model(field.schema))
        # Add other field types as needed
        else:
            raise NotImplementedError(f"Field type {type(field)} not supported")

    return api.model(schema.__name__, model_fields)