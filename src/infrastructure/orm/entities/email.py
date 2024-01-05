from .base_entity import BaseEntity
from sqlalchemy import Column, String, Integer, ForeignKey

class Email(BaseEntity):
    __tablename__ = "emails"
    
    email_address = Column("email_address", String(50))
    person_id = Column(Integer, ForeignKey("people.id"))