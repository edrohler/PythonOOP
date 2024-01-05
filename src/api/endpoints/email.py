from flask import request
from flask_restx import Resource, Namespace, fields
from src.core.domain.viewmodels import Email

def create_email_model(api):
    return api.model('Email', {
        'email_address': fields.String(required=True, description='Email address'),
        'person_id': fields.Integer(required=True, description='Person ID')
    })

def create_email_ns(api, uow, version):
    ns = Namespace(f"Email Endpoints", description="Email API", path=f"/api/v{version}/email")
    email_model = create_email_model(api)
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
                data = api.payload
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
            data = request.json
            uow.email_repository.update(id, **data)
            return {"message": "Email updated"}, 200
        
        def delete(self, id):
            """Delete an email."""
            uow.email_repository.delete(id)
            return {"message": "Email deleted"}, 200
        
        
    return ns