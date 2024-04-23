from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = 'authentication_user'

    email = Column(String, primary_key=True)
    name = Column(String(100))

class Post(Base):
    __tablename__ = 'posts_post'

    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    subheading = Column(String(1000))
    user_id = Column(String)
    content = Column(Text)
    image = Column(String)
    updated = Column(DateTime)
    tag = Column(String(15))