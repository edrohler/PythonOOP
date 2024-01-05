from flask import request
from flask_restx import Resource, Namespace
from src.api.schemas.person import PersonSchema
from src.api.utils import schema_to_model
from src.core.domain.models import Person
from src.core.services.logging_service import LoggingService

def create_person_ns(api,uow,version, logger: LoggingService):
    ns = Namespace(f"Person Endpoints", description="Person API", path=f"/api/v{version}/person")
    person_api_model = schema_to_model(PersonSchema, api)
    @ns.route("/")
    class PeopleList(Resource):
        def get(self):
            """Get all persons."""
            persons = uow.person_repository.get_all()
            result = PersonSchema(many=True).dump(persons)
            return persons
        
        @ns.expect(person_api_model, validate=True)
        def post(self):
            """Create a new person."""            
            try:
                data = PersonSchema().load(request.json)
                person = Person(**data)
                uow.person_repository.add(person)
                uow.commit()
                return {"message": "Person created"}, 201
            except Exception as e:
                logger.log_error(e)
                return {"message": "An Error Occurred"}, 400
        
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
            try:
                data = api.payload
                uow.person_repository.update(id, **data)
                return {"message": "Person updated"}, 200
            except Exception as e:
                return {"message": str(e)}, 400
        
        def delete(self, id):
            """Delete a person."""
            uow.person_repository.delete(id)
            return {"message": "Person deleted"}, 200
            
    return ns