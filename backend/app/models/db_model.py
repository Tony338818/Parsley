from sqlalchemy import String, Integer, create_engine, Column, Text, DateTime, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# create engine
engine = create_engine('sqlite:///./app.db')

# bind the session
Session = sessionmaker(bind=engine)

# create an object of the session
session = Session()

# base template for tables
Base = declarative_base()

# Creating tables 
class User(Base):
    __tablename__ = 'Users'

    id = Column(Integer, unique=True, primary_key=True, index=True)
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    password = Column(Text, nullable=False)
    createdAt = Column(DateTime, default=func.now(), nullable=False)


# Creating the tables
Base.metadata.create_all(bind=engine)
# Base.metadata.drop_all(bind=engine)