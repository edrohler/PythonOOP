from marshmallow import fields
from marshmallow_dataclass import class_schema
from src.core.domain.models.email import Email

EmailSchema = class_schema(Email)

class EmailApiSchema(EmailSchema):
    id = fields.Integer()
    email_address = fields.String(required=True)
    person_id = fields.Integer(required=True)
    # class Meta:
    #     ordered = True
    #     unknown = "EXCLUDE"