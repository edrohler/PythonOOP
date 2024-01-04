from flask import Blueprint, request
from flask_restx import Api, Resource, Namespace
from src.core.domain.viewmodels import Person

def create_person_ns(uow,version):
    ns = Namespace(f"People Endpoints", description="Person API", path=f"/people")

    @ns.route("/")
    class PeopleList(Resource):
        def get(self):
            """Get all people."""
            persons = uow.person_repository.get_all()
            return persons
        
        def post(self):
            """Create a new person."""
            data = request.json
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