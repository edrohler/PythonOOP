class GenericRepository:
    def __init__(self, session, model):
        self.session = session
        self.model = model

    def add(self, entity):
        self.session.add(entity)

    def get_by_id(self, id):
        return self.session.query(self.model).filter_by(id=id).one_or_none()

    def get_all(self):
        return self.session.query(self.model).all()

    def delete(self, entity):
        self.session.delete(entity)

    def update(self):
        self.session.commit()
