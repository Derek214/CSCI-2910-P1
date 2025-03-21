from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base
from pydantic import BaseModel

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    image_url = Column(String)
    is_admin = Column(Boolean)

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    title = Column(String)
    post_text = Column(String)
    likes = Column(Integer, default=0)
    

class PostUpdate(BaseModel):
    title: str
    post_text: str
    
    
class UserCreate(BaseModel):
    username: str
    image_url: str
    is_admin: bool = False

class PostCreate(BaseModel):
    user_id: int
    title: str
    post_text: str

class UserUpdate(BaseModel):
    username: str
    image_url: str
    is_admin: bool