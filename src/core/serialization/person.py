from marshmallow import fields
from marshmallow_dataclass import class_schema
from src.core.domain.models.person import Person

PersonSchema = class_schema(Person)

class PersonApiSchema(PersonSchema):
    id = fields.Integer()
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    gender = fields.String(required=True, metadata={'length': 1})
    age = fields.Integer(required=True)
    # email = fields.Nested("EmailApiSchema", many=True)
    # address = fields.Nested("AddressApiSchema", many=True)
    # class Meta:
    #     ordered = True
    #     unknown = "EXCLUDE"