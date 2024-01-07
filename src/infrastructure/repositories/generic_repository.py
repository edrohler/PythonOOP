from src.core.services.logging_service import LoggingService

class GenericRepository:
    def __init__(self, session, model, logger: LoggingService=None):
        self.session = session
        self.model = model
        self.logger = logger

    def add(self, entity):
        self.session.add(entity)
        self.logger.log_info(f'Added entity of type {type(entity).__name__} to session')

    def get_by_id(self, id):
        result = self.session.query(self.model).filter_by(id=id).one_or_none()
        if result:
            self.logger.log_info(f'Fetched entity with id {id} from {self.model.__name__}')
        else:
            self.logger.log_info(f'No entity with id {id} found in {self.model.__name__}')
        return result

    def get_all(self):
        self.logger.log_info(f'Fetched all entities from {self.model.__name__}')
        return self.session.query(self.model).all()

    def delete(self, entity):
        entity_to_delete = self.get_by_id(entity.id)
        if entity_to_delete:
            try:
                self.session.delete(entity)
                self.logger.log_info(f'Deleted entity of type {type(entity).__name__} from session')
                return entity
            except Exception as e:
                self.session.rollback()
                self.logger.log_error(f'Error deleting entity: {e}')
                raise
        else:
            self.logger.log_info(f'Entity with ID {entity.id} not found')

    def update(self, entity):
        # Get the existing entity from the database
        entity_to_update = self.get_by_id(entity.id)

        if entity_to_update:
            try:
                self.session.merge(entity)
                self.session.commit()
                self.logger.log_info(f'Updated entity with ID {entity.id}')
                return entity
            except Exception as e:
                self.session.rollback()
                self.logger.log_error(f'Error updating entity: {e}')
                raise
        else:
            self.logger.log_info(f'Entity with ID {entity.id} not found')
