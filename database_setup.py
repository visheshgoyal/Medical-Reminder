from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key = True)
    name = Column(String(50), nullable = False)
    email = Column(String(100))
    age = Column(Integer, nullable = False)
    detail = Column(String(250), nullable = False)
    number = Column(Integer, nullable = False)
    
    @property
    def serialize(self):
        return {
            'id' : self.id,
            'name'  : self.name,
            'email' : self.email,
            'detail' : self.detail,
            'number' : self.number
        }

engine = create_engine('sqlite:///medreminder.db')


Base.metadata.create_all(engine)
