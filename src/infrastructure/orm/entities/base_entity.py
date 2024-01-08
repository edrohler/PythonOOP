from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class BaseEntity(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, nullable=False)
    created_by = Column(String, nullable=False)
    updated_at = Column(DateTime, nullable=True)
    updated_by = Column(String, nullable=True)