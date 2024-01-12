from .base_entity import BaseEntity
from sqlalchemy import Column, String, Integer, ForeignKey


class Address(BaseEntity):
    __tablename__ = "addresses"
    
    address_line_1 = Column("address_line_1", String(120)) 
    address_line_2 = Column("address_line_2", String(50), nullable=True, default=None)
    city = Column("city", String(100))
    state = Column("state", String(2))
    zip_code = Column("zipcode", String(5))
    person_id = Column(Integer, ForeignKey('people.id'))