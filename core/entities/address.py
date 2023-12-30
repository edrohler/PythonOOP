
from .base import Base, Column, String, Integer, ForeignKey


class Address(Base):
    __tablename__ = "addresses"
    
    address_line_1 = Column("address_line_1", String(120)) 
    address_line_2 = Column("address_line_2", String(50))
    city = Column("city", String(100))
    state = Column("state", String(2))
    zipcode = Column("zipcode", String(5))
    person_id = Column(Integer, ForeignKey('people.id'))
    
    def __init__(self, address_line_1, address_line_2, city, state, zipcode, person_id):
        self.address_line_1 = address_line_1
        self.address_line_2 = address_line_2
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.person_id = person_id