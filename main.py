from models import Base, User, Post
from fastapi import FastAPI, Depends, Query, HTTPException
from sqlalchemy import create_engine, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL = "sqlite:///./social_media.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

@app.get("/users/")
def get_users(name: str = Query(None), db: Session = Depends(get_db)):
    query = select(User)
    if name:
        query = query.filter(User.username == name)
    users = db.execute(query).scalars().all()
    return users

@app.get("/users/{user_id}")
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.execute(select(User).filter(User.id == user_id)).scalars().first()
    if user is None:
        return {"error": "User not found"}
    return user

@app.get("/posts/")
def get_users(db: Session = Depends(get_db)):
    query = select(Post)
    posts = db.execute(query).scalars().all()
    return posts
