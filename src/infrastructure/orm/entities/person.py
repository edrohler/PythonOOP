from .base_entity import BaseEntity
from sqlalchemy import CHAR, Column, Integer, String
from sqlalchemy.orm import relationship

class Person(BaseEntity):
    __tablename__ = "people"
    
    firstname = Column(String(50))
    lastname = Column(String(50))
    gender = Column(CHAR(1))
    age = Column(Integer)
    addresses = relationship("Address", backref="person")
    emails = relationship("Email", backref="person")