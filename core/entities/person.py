from .base import Base, CHAR, Column, Integer, String, relationship

class Person(Base):
    __tablename__ = "people"
    
    firstname = Column("firstname", String(50))
    lastname = Column("lastname", String(50))
    gender = Column("gender", CHAR(1))
    age = Column("age", Integer)
    addresses = relationship("Address", backref="person")
    emails = relationship("Email", backref="person")
    
    
    def __init__(self, ssn, firstname, lastname, gender, age):
        self.ssn = ssn
        self.firstname = firstname
        self.lastname = lastname
        self.gender = gender
        self.age = age