from flask import request
from flask_restx import Resource, Namespace, fields
from src.core.domain.viewmodels import Person

def create_person_model(api):
    return api.model('Person', {
        'first_name': fields.String(required=True, description='First name'),
        'last_name': fields.String(required=True, description='Last name'),
        'age': fields.Integer(required=True, description='Age')
    })

def create_person_ns(api,uow,version):
    ns = Namespace(f"Person Endpoints", description="Person API", path=f"/api/v{version}/person")
    person_model = create_person_model(api)
    @ns.route("/")
    class PeopleList(Resource):
        def get(self):
            """Get all persons."""
            persons = uow.person_repository.get_all()
            return persons
        
        @ns.expect(person_model, validate=True)
        def post(self):
            """Create a new person."""
            data = api.payload
            person = Person(**data)
            uow.person_repository.add(person)
            uow.commit()
            return {"message": "Person created"}, 201
        
    @ns.route("/<int:id>")
    class PeopleResource(Resource):
        def get(self, id):
            """Get a person by ID."""
            person = uow.person_repository.get_by_id(id)
            if person is None:
                return {"message": "Person not found"}, 404
            return person

        def put(self, id):
            """Update an existing person."""
            data = request.json
            uow.person_repository.update(id, **data)
            return {"message": "Person updated"}, 200
        
        def delete(self, id):
            """Delete a person."""
            uow.person_repository.delete(id)
            return {"message": "Person deleted"}, 200
            
    return ns