from .base import Base, Column, String, Integer, ForeignKey

class Email(Base):
    __tablename__ = "emails"
    
    email = Column("email", String(50))
    person_id = Column(Integer, ForeignKey("people.id"))
    
    def __init__(self, email, person_id):
        self.email = email
        self.person_id = person_id