from models import Base, User, Post, PostUpdate, UserCreate, PostCreate, UserUpdate
from fastapi import FastAPI, Depends, Query, HTTPException 
from sqlalchemy import create_engine, select, update, delete
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
def get_users(name: str, db: Session = Depends(get_db)):
    query = select(User)
    if name:
        query = query.filter(User.username == name)
    users = db.execute(query).scalars().all()
    return users

@app.get("/users/{user_id}")
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.execute(select(User).filter(User.id == user_id)).scalars().first()
    return user

@app.get("/posts/")
def get_posts(db: Session = Depends(get_db)):
    query = select(Post)
    posts = db.execute(query).scalars().all()
    return posts

@app.get("/posts/{post_id}")
def get_posts_by_id(post_id: int, db: Session = Depends(get_db)):
    post = db.execute(select(Post).filter(Post.id == post_id)).scalars().first()
    return post

@app.patch("/posts/{post_id}/increment_likes")
def increment_post_likes(post_id: int, db: Session = Depends(get_db)):
    post = db.execute(select(Post).filter(Post.id == post_id)).scalars().first()
    
    db.execute(update(Post).where(Post.id == post_id).values(likes=post.likes + 1))
    db.commit()
    return {"message": "Likes incremented", "post_id": post_id, "likes": post.likes + 1}

@app.patch("/posts/{post_id}/decrement_likes")
def increment_post_likes(post_id: int, db: Session = Depends(get_db)):
    post = db.execute(select(Post).filter(Post.id == post_id)).scalars().first()
    
    db.execute(update(Post).where(Post.id == post_id).values(likes=post.likes - 1))
    db.commit()
    return {"message": "Likes incremented", "post_id": post_id, "likes": post.likes - 1}


@app.get("/posts/user/{user_id}")
def get_posts_by_user(user_id: int, db: Session = Depends(get_db)):
    posts = db.execute(select(Post).filter(Post.user_id == user_id)).scalars().all()
    return posts

@app.put("/posts/{post_id}")
def update_post(post_id: int, post_update: PostUpdate, db: Session = Depends(get_db)):
    
    db.execute(update(Post).where(Post.id == post_id).values(post_text=post_update.post_text))
    db.commit()
    
    return {"message": "Post updated successfully", "post_id": post_id, "post_text": post_update.post_text}

@app.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(username=user.username, image_url=user.image_url, is_admin=user.is_admin)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully", "user_id": new_user.id}

@app.post("/posts/")
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    new_post = Post(user_id=post.user_id, title=post.title, post_text=post.post_text, likes=0)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"message": "Post created successfully", "post_id": new_post.id}

@app.delete("/posts/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)): 
    db.execute(delete(Post).where(Post.id == post_id))
    db.commit()
    
    return {"message": "Post deleted successfully", "post_id": post_id}

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db.execute(delete(User).where(User.id == user_id))
    db.commit()
    
    return {"message": "User deleted successfully", "user_id": user_id}

@app.put("/users/{user_id}")
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    
    db.execute(update(User).where(User.id == user_id).values(
        username=user_update.username,
        image_url=user_update.image_url,
        is_admin=user_update.is_admin
    ))
    db.commit()
    
    return {"message": "User updated successfully", "user_id": user_id}