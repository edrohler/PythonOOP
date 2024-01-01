from src.core.services.logging_service import LoggingService

class GenericRepository:
    def __init__(self, session, model):
        self.session = session
        self.model = model
        self.logger = LoggingService(self.__class__.__name__)

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
        self.session.delete(entity)
        self.logger.log_info(f'Deleted entity of type {type(entity).__name__} from session')

    def update(self):
        self.session.commit()
        self.logger.log_info(f'Updated session')
