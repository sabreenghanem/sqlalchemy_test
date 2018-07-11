import sqlalchemy

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, exists
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer, String, DateTime, Enum, Float, Text

Base=declarative_base()

class User(Base):
	__tablename__="user"
	id=Column(Integer,primary_key=True)
	first_name=Column(String)
	surname=Column(String)
	email=Column(String)
	date_of_birth=Column(DateTime)
	phone=Column(String)
	gender=Column(Enum('male','female'))
	password=Column(String)
	country_code_lookup_id=Column(Integer,ForeignKey('country_code_lookup.id'))
	country_code_lookup=relationship('CountryCodeLookup',back_populates='user')
	user_general_info=relationship('UserGeneralInfo',back_populates='user')

class UserGeneralInfo(Base):
	__tablename__="user_general_info"
	id=Column(Integer,primary_key=True)
	hight=Column(Float)
	weight=Column(Float)
	marital_status=Column(Enum('Married','single','divorced','widowed'))
	registered_treatment=Column(Text)
	created=Column(DateTime)
	updated=Column(DateTime)
	user_id=Column(Integer,ForeignKey('user.id'))
	user=relationship('User',back_populates='user_general_info')

class CountryCodeLookup(Base):
	__tablename__="country_code_lookup"
	id=Column(Integer,primary_key=True)
	iso=Column(String)
	name=Column(String)
	nice_name=Column(String)
	iso3=Column(String)
	number_code=Column(Integer)
	flag=Column(String)
	created=Column(DateTime)
	updated=Column(DateTime)
	user=relationship('User',back_populates='country_code_lookup')

class Main():

	def __init__(self):
       pass 

    def __del__(self):
       pass


    def run(self):




















if __name__=='__main__' or __name__=='user_test.py':

	engine = create_engine('mysql://root:password@localhost:3306/user_test',echo=False)
	connection = engine.connect()
	Session = sessionmaker(bind=engine)
	session = Session()

	Main().run()
	connection.close()



