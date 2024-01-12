from flask import request
from flask_restx import Resource, Namespace
from src.api.utils import schema_to_api_model
from src.core.serialization.email import EmailSchema
from src.core.services.logging_service import LoggingService
from src.core.services.email_service import EmailService
from src.infrastructure.unit_of_work import UnitOfWork

def create_email_ns(api, uow: UnitOfWork, version, logger: LoggingService):
    ns = Namespace(f"Email Endpoints", description="Email API", path=f"/api/v{version}/email")
    email_model = schema_to_api_model(EmailSchema, api)
    email_service = EmailService(uow)
    @ns.route("/")
    class EmailList(Resource):
        def get(self):
            """Get all emails."""
            emails = email_service.get_all_emails()
            return EmailSchema(many=True).dump(emails)
        
        @ns.expect(email_model, validate=True)
        def post(self):
            """Create a new email."""
            try:
                email = EmailSchema().load(request.json)
                email_service.create_email(email)
                return {"message": "Email created"}, 201
            except Exception as e:
                logger.log_error(e)
                return {"message": "An Error Occurred"}, 400
            
        @ns.expect(email_model, validate=True)
        def put(self):
            """Update an existing email."""
            if "id" == None or "id" not in request.json:
                return {"message": "Id is required"}, 400
            try:
                email = EmailSchema().load(request.json)
                updated_email = email_service.update_email(email)
                if updated_email is None:
                    return {"message": "Error updating email"}, 400
                return {"message": "Email updated"}, 200
            except Exception as e:
                logger.log_error(e)
                return {"message": "Error updating email"}, 400
        
    @ns.route("/<int:id>")
    class EmailResource(Resource):
        def get(self, id):
            """Get an email by ID."""
            email = email_service.get_email_by_id(id)
            if email is None:
                return {"message": "Email not found"}, 404
            return EmailSchema().dump(email)
        
        
        def delete(self, id):
            """Delete an email."""
            try:
                deleted_email = email_service.delete_email(id)
                if deleted_email is None:
                    return {"message": "Email not found"}, 404
                return {"message": f"Email with id: {id} deleted"}, 200
            except Exception as e:
                logger.log_error(e)
                return {"message": "Error deleting email"}, 400        
        
    return ns