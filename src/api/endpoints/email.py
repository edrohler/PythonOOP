from flask import Blueprint, request
from flask_restx import Api, Resource, Namespace
from src.core.domain.viewmodels import Email

def create_email_ns(uow, version):
    ns = Namespace(f"Email Endpoints", description="Email API", path=f"/api/v{version}/email")
    
    @ns.route("/")
    class EmailList(Resource):
        def get(self):
            """Get all emails."""
            emails = uow.email_repository.get_all()
            return emails
        
        def post(self):
            """Create a new email."""
            data = request.json
            email = Email(**data)
            uow.email_repository.add(email)
            uow.commit()
            return {"message": "Email created"}, 201
        
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
            data = request.json
            uow.email_repository.update(id, **data)
            return {"message": "Email updated"}, 200
        
        def delete(self, id):
            """Delete an email."""
            uow.email_repository.delete(id)
            return {"message": "Email deleted"}, 200
        
        
    return ns