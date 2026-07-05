from random import randrange
from typing import Optional, List
from fastapi import FastAPI, HTTPException, Response, status, Depends
from httpx import post
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
import time
from app.routers import posts
from . import model, schemas, utils 
from . database import engine, get_db
from .routers import posts, user, auth


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

app.include_router(posts.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"Message": "Hi, Welcome to my API "}

