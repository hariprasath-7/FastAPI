from fastapi import FastAPI, HTTPException, Response, status, Depends
from httpx import post
from app.routers import posts
from . import model 
from . database import engine
from .routers import posts, user, auth, vote
from . config import settings
from fastapi.middleware.cors import CORSMiddleware

# model.Base.metadata.create_all(bind=engine)
origins = []

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins= origins ,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)


app.include_router(posts.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"Message": "Hi, Welcome to my API "}

