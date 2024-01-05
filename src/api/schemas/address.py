from marshmallow import fields
from marshmallow_dataclass import class_schema
from src.core.domain.models.address import Address

AddressSchema = class_schema(Address)

class AddressApiSchema(AddressSchema):
    id = fields.Integer()
    street = fields.String(required=True)
    city = fields.String(required=True)
    state = fields.String(required=True)
    zip_code = fields.String(required=True)
    person_id = fields.Integer(required=True)
    # class Meta:
    #     ordered = True
    #     unknown = "EXCLUDE"