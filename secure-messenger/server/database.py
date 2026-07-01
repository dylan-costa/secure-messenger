#Database connection and setup


from sqlalchemy import create_engine #database connection
from sqlalchemy.orm import sessionmaker, declarative_base



DATABASE_URL = "sqlite:///./secure_messenger.db"
#engine = create_engine(DATABASE_URL)
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}
) #connect to the database

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) #create a session
Base = declarative_base() #create a base class for the models


