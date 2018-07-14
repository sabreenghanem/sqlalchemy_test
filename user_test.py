import sqlalchemy

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, exists
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer, String, DateTime, Enum, Float, Text
from sqlalchemy.orm import aliased , joinedload
from sqlalchemy import text
from sqlalchemy import func

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
	def __repr__(self):
		return "<User(first_name='%s',surname='%s')>"%(self.first_name,self.surname)


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
	def __repr__(self):
		return "<CountryCodeLookup(name='%s',nice_name='%s')>"%(self.name,self.nice_name)

class Main():

	# def __init__(self):
 #        pass 

 #    def __del__(self):
 #        pass


    def run(self):
        #select
    	our_country=session.query(CountryCodeLookup).filter_by(iso='AL').first()
    	print (our_country)

        #INSERT
    	ed_user=User(first_name="ed",surname="Ed Jones",email="ed@gmail.com",date_of_birth="1991-03-05 00:00:00",phone="0569123584",gender="male",password="jihhf") #transient
    	ed_user.country_code_lookup=our_country
    	session.add(ed_user) #instance is pending  
    	session.commit() #persistent

        #INSERT more objects at once using add_all()
    	session.add_all([
    		User(first_name="u1",surname="user one",email="u1@example.net",password="jfiufdgiu"),
    		User(first_name="u2",surname="user tow",email="u2@example.net",password="uuuuu2"),
    		User(first_name="u3",surname="user three",email="u3@gmail.com",password="uuuu3")])
    	session.commit()

    	#Rolling Back
    	ed_user.first_name="Edwardo"
    	fake_user=User(first_name="fakeusder",surname="Invalid",password="12345")
    	session.add(fake_user)
    	ss=session.query(User).filter(User.first_name.in_(["Edwardo","fakeusder"])).all()
    	print(ss)  #output [<User(first_name='Edwardo',surname='Ed Jones')>, <User(first_name='fakeusder',surname='Invalid')>]

    	session.rollback()
    	print(ed_user.first_name) #output 'ed'
    	print(fake_user in session) #output False

    	bss=session.query(User).filter(User.first_name.in_(['ed','fakeusder'])).all()
    	print(bss) #output [<User(first_name='ed',surname='Ed Jones')>]


    	#Querying

    	for instance in session.query(User).order_by(User.id): #127 u3 user three ...
    		print(instance.id, instance.first_name, instance.surname)

    	for row in session.query(User,User.first_name).all(): #<User(first_name='u3',surname='user three')> u3 ...
    		print(row.User,row.first_name)

    	for row in session.query(User.first_name.label('name_label')).all(): # u3 ...
    		print(row.name_label)


    	# aliased
    	user_alias = aliased(User,name='user_alias')
    	for row in session.query(user_alias, user_alias.first_name).all():
    		print(row.user_alias)

    	# Python array slices
    	for u in session.query(User).order_by(User.id)[1:3]:
    		print(u)

    	#filtering results using filter_by
    	for name in session.query(User.first_name).filter_by(surname="Ed Jones"):
    		print (name) # output 'ed'

    	#filtering using filter()
    	for user in session.query(User).filter(User.first_name=="ed"):
    		print(user)  #output <User(first_name='ed',surname='Ed Jones')>

    	# Textual SQL 
    	for user in session.query(User).filter(text("id<7")).order_by(text("id")).all():
    		print(user.first_name)

    	#from_statement()
    	q=session.query(User).from_statement(text("SELECT * FROM user WHERE first_name=:name")).params(name='ed').all()
    	print(q) #output [<User(first_name='ed',surname='Ed Jones')>]

    	#Counting
    	print(session.query(User).filter(User.first_name.like('%ed')).count()) 

    	# Querying with joins
    	join_query=session.query(User).join(UserGeneralInfo,User.id==UserGeneralInfo.user_id).all()
    	print(join_query)

    	#using exists
    	stmt=exists().where(UserGeneralInfo.user_id==User.id)
    	for name in session.query(User.first_name).filter(stmt):
    		print(name)

    	#joined load
    	sabreen = session.query(User).options(joinedload(User.country_code_lookup)).filter_by(first_name='sabreen').one()
    	print(sabreen)
    	print(sabreen.country_code_lookup)

    	#DELETE
    	session.query(User).filter_by(email="yamen@gmail.com").delete()
    	session.commit()



if __name__=='__main__' or __name__=='user_test.py':

	engine = create_engine('mysql://root:password@localhost:3306/user_test',echo=False)
	connection = engine.connect()
	Session = sessionmaker(bind=engine)
	session = Session()

	Main().run()
	connection.close()



