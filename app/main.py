from random import randrange
from typing import Optional, List
from fastapi import FastAPI, HTTPException, Response, status, Depends
from httpx import post
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
import time
from . import model, schemas
from . database import engine, get_db

model.Base.metadata.create_all(bind=engine)

app = FastAPI()

# while True:
    
try:
        conn = psycopg2.connect(host='localhost', database='fastapi',  user='postgres', password='2006',cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful")
        # break
except Exception as error:
        print("Connecting to database failed ")
        print("Error:", error)
        time.sleep(2)

    

my_posts = [
    {"title": "title of posts 1", "content": "content of post 1 ", "id": 1 },
    {"title": "favorite foods", "content": "I like pizza", "id": 2}
]

def find_index_post(id: int):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i
    return None

def find_post(id: int):
    for p in my_posts:
        if p['id'] == id:
            return p
    return None

@app.get("/")
def root():
    return {"Message": "Hi, Welcome to my API "}

@app.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts """)
    # posts= cursor.fetchall()
    posts = db.query(model.Post).all()
    return posts

@app.post("/createposts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    # new_post =cursor.fetchone()
    # conn.commit()
    new_post = model.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db), response_model=schemas.Post):
    # cursor.execute("""SELECT * from posts WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()
    post = db.query(model.Post).filter(model.Post.id == id).first()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found"
        )
    return  post

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT) 
def delete_post(id: int, db : Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts where id = %s returning *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post = db.query(model.Post).filter(model.Post.id == id)
    if post.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist"
        )
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), response_model=schemas.Post):
    # cursor.execute("""UPDATE posts SET title = %s , content = %s, published = %s WHERE id = %s RETURNING * """,(post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(model.Post).filter(model.Post.id == id)
    post =post_query.first()
    
    if post is None: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} does not exist")
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()

@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate,db: Session = Depends(get_db)):
    new_user = model.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

    