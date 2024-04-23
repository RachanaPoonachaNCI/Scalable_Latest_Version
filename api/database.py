from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import SQLALCHEMY_DATABASE_URL
# Create connection to database

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

Base = declarative_base()
SessionMaker = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionMaker()