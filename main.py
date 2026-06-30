from random import randrange
from typing import Optional
from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [
    {"title": "title of posts 1", "content": "content of post 1 ", "id": 1 },
    {"title": "favorite foods", "content": "I like pizza", "id": 2}
]

def find_index_post(id):
    for i , p in enumerate(my_posts):
        if p['id'] == id:
            return i

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

@app.get("/")
def root():
    return {"Message": "Hi, Welcome to my API "}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/createposts")
def create_posts(new_post: Post):
    post_dict = new_post.dict() 
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": my_posts}

@app.get("/posts/{id}")
def get_post(id: int, response: Response):

    post = find_post(int(id))
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found")
    return {"post_detail": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT) 
def delete_post(id: int):
    index = find_index_post(id)
    if index == None:
        raise HTTPExecution(status_code=status.HTTP.404_NOT_FOUND,detail = f"post with id: {id} does not exists")
    my_posts.pop(index)
    return {"message": "post was successfully deleted"}
