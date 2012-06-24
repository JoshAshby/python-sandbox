from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

import itsdangerous
from itsdangerous import Serializer
import string
import random

secretKey = "33DJ89SQICUP9C5KRL16WHOYTY08FA430OM3YOFVXOW2PSYN8JSVIGWLVM60RDDQHXD7PT4IUTT8E3DTOD6DVAAH002BHBRECJEC"

engine = create_engine('mysql://josh:joshmysql@localhost/test')

Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()


class User(Base):
	__tablename__ = 'users'

	id = Column(Integer, primary_key=True)
	name = Column(String(100))
	password = Column(String(500))
	salt = Column(String(100))


user = session.query(User).filter_by(name="Josh").first()

salt = user.salt

signer = Serializer(secretKey, salt=salt)

passwordOld = "super new car"
password = "test"

passwd = signer.dumps(password).split(".")[1]

oldPass = user.password

if signer.loads("\"" + passwordOld + "\"." + oldPass):
	print True

	user.password = passwd

session.commit()

