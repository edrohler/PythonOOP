from sqlalchemy import Column, CHAR, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

class Base():
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)

Base = declarative_base(cls=Base)