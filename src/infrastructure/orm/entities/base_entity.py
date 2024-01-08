import datetime
from sqlalchemy import Column, DateTime, Integer, String, event
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class BaseEntity(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    created_by = Column(String, nullable=False)
    updated_at = Column(DateTime, onupdate=datetime.datetime.utcnow, nullable=True)
    updated_by = Column(String, nullable=True)
