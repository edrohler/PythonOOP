from .base_entity import BaseEntity
from sqlalchemy import CHAR, Column, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

class Person(BaseEntity):
    __tablename__ = "people"
    __table_args__ = (UniqueConstraint('firstname', 'lastname'),)
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    
    gender = Column(CHAR(1))
    age = Column(Integer)
    addresses = relationship("Address", backref="person")
    emails = relationship("Email", backref="person")