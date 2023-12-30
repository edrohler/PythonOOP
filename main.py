
from core.models import Base, Person
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///database.db', echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

person1 = Person("123456789", "John", "Doe", "M", 30)
person2 = Person("789456123", "Jane", "Doe", "F", 40)
person3 = Person("987654321", "Will", "Doe", "M", 50)
session.add(person1)
session.add(person2)
session.add(person3)
session.commit()
