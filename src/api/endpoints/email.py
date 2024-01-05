from flask import request
from flask_restx import Resource, Namespace
from src.api.schemas.email import EmailSchema
from src.api.utils import schema_to_model
from src.core.domain.models import Email
from src.core.services.logging_service import LoggingService

def create_email_ns(api, uow, version, logger: LoggingService):
    ns = Namespace(f"Email Endpoints", description="Email API", path=f"/api/v{version}/email")
    email_model = schema_to_model(EmailSchema, api)
    @ns.route("/")
    class EmailList(Resource):
        def get(self):
            """Get all emails."""
            emails = uow.email_repository.get_all()
            return emails
        
        @ns.expect(email_model, validate=True)
        def post(self):
            """Create a new email."""
            try:
                data = EmailSchema().load(request.json)
                email = Email(**data)
                uow.email_repository.add(email)
                uow.commit()
                return {"message": "Email created"}, 201
            except Exception as e:
                return {"message": str(e)}, 400
        
    @ns.route("/<int:id>")
    class EmailResource(Resource):
        def get(self, id):
            """Get an email by ID."""
            email = uow.email_repository.get_by_id(id)
            if email is None:
                return {"message": "Email not found"}, 404
            return email
        
        def put(self, id):
            """Update an existing email."""
            data = api.payload
            uow.email_repository.update(id, **data)
            return {"message": "Email updated"}, 200
        
        def delete(self, id):
            """Delete an email."""
            uow.email_repository.delete(id)
            return {"message": "Email deleted"}, 200
        
        
    return ns