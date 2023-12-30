
from sqlalchemy import CHAR, Column, Integer, String
from core.models.base import Base

class Person(Base):
    __tablename__ = "people"
    
    ssn = Column("ssn", String(9), primary_key=True)
    firstname = Column("firstname", String(50))
    lastname = Column("lastname", String(50))
    gender = Column("gender", CHAR)
    age = Column("age", Integer)
    
    def __init__(self, ssn, firstname, lastname, gender, age):
        self.ssn = ssn
        self.firstname = firstname
        self.lastname = lastname
        self.gender = gender
        self.age = age
        
    def __repr__(self):
        return f"({self.ssn}) {self.firstname} {self.lastname} ({self.gender},{self.age})"