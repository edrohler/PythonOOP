import datetime
from sqlalchemy import Column, DateTime, Integer, String, event
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class BaseEntity(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=True)
    created_by = Column(String, nullable=True)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=True)
    updated_by = Column(String, nullable=True)
    
#     @staticmethod
#     def before_insert_listener(mapper, connection, target):
#         target.created_at = datetime.datetime.utcnow()
#         target.created_by = connection.info.get("user", "system")

#     @staticmethod
#     def before_update_listener(mapper, connection, target):
#         target.updated_at = datetime.datetime.utcnow()
#         target.updated_by = connection.info.get("user", "system")

# event.listen(BaseEntity, 'before_update', BaseEntity.before_update_listener)
# event.listen(BaseEntity, 'before_insert', BaseEntity.before_insert_listener)