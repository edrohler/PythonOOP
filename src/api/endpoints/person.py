from flask import request
from flask_restx import Resource, Namespace
from src.api.utils import schema_to_api_model
from src.core.services.logging_service import LoggingService
from src.core.serialization.person import PersonSchema
from src.core.services.person_service import PersonService
from src.infrastructure.unit_of_work import UnitOfWork

def create_person_ns(api,uow: UnitOfWork,version, logger: LoggingService):
    ns = Namespace(f"Person Endpoints", description="Person API", path=f"/api/v{version}/person")
    person_api_model = schema_to_api_model(PersonSchema, api)
    person_service = PersonService(uow)
    @ns.route("/")
    class PeopleList(Resource):
        def get(self):
            """Get all persons."""
            persons = person_service.get_all_people()
            result = PersonSchema(many=True).dump(persons)
            return result
        
        @ns.expect(person_api_model, validate=True)
        def post(self):
            """Create a new person."""            
            try:
                person = PersonSchema().load(request.json)
                person_service.create_person(person)
                return {"message": "Person created"}, 201
            except Exception as e:
                logger.log_error(e)
                return {"message": "An Error Occurred"}, 400
        
        @ns.expect(person_api_model, validate=True)
        def put(self):
            """Update an existing person."""
            if "id" == None or "id" not in request.json:
                return {"message": "Id is required"}, 400
            try:
                person = PersonSchema().load(request.json)
                updated_person = person_service.update_person(person)
                if updated_person is None:
                    return {"message": "Error updating person"}, 400
                return {"message": "Person updated"}, 200
            except Exception as e:
                logger.log_error(e)
                return {"message": "Error updating person"}, 400

    @ns.route("/<int:id>")
    class PeopleResource(Resource):
        def get(self, id):
            """Get a person by ID."""
            person = person_service.get_person_by_id(id)
            if person is None:
                return {"message": "Person not found"}, 404
            return PersonSchema().dump(person)

        
        def delete(self, id):
            """Delete a person."""
            try:
                deleted_person = person_service.delete_person(id)
                if deleted_person is None:
                    return {"message": "Person not found"}, 404
                return {"message": f"Person with id: {id} deleted"}, 200
            except Exception as e:
                logger.log_error(e)
                return {"message": "Error delting person"}, 400
            
    return ns