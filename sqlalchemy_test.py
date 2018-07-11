import sqlalchemy

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, exists
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer, String

Base = declarative_base()

class User(Base):
  __tablename__ = 'user'
  id = Column(Integer,primary_key=True)
  name = Column(String,nullable=False)
  email = Column(String,nullable=False,unique=True)
  nick = Column(String)
  address_id = Column(Integer, ForeignKey('address.id'))
  address = relationship("Address", back_populates="user")

class Address(Base):
  __tablename__ = 'address'
  id = Column(Integer,primary_key=True)
  street = Column(String,nullable=False)
  city = Column(String,nullable=False)

  user = relationship('User',back_populates="address")

  def __init__(self, city='Ramallah'):
      self.city = city

class Main():
   
   def __init__(self):
     pass

   def __del__(self):
     pass

   def run(self):

     if not session.query(exists().where(User.email == 'test@example.net')).scalar():
       u1 = User()
       u1.name = "Test user"
       u1.email = "test@example.net"

       a1 = Address()
       a1.street = "str 526"
       a1.city = "city 526"

       u1.address = a1
       session.add(a1)
       session.add(u1)
       session.commit()

     if session.query(exists().where(Address.city == 'city 526')).scalar():
      a2 = session.query(Address).filter_by(city='city 526').first()
      print(a2.city)

     if session.query(exists().where(User.email=='test@example.net')).scalar():
      u = session.query(User).filter_by(email='test@example.net').first()
      u.nick = "b"
      session.commit()

     if session.query(exists().where(User.email =='sabreen@gmail.com')).scalar():
      session.query(User).filter_by(email='sabreen@gmail.com').delete()
      session.commit()

     if session.query(exists().where(Address.city == 'Tulkarm')).scalar():
      session.query(Address).filter_by(city='Tulkarm').delete()
      session.commit()

if __name__=='__main__' or __name__=='sqlalchemy_test':

   engine = create_engine('mysql://root:password@localhost:3306/sqlalchemy_test',echo=False)
   connection = engine.connect()
   Session = sessionmaker(bind=engine)
   session = Session()
   
   Main().run()
   connection.close()