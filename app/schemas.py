from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id : int 
    created_at: datetime
    owner_id : int

    class Config:
        form_attribute = True

class UserCreate(BaseModel):
    email : str
    password : str

class UserOut(BaseModel):
    id : int
    email : str
    created_at : datetime

    class Config:
        form_attribute = True

class UserLogin(BaseModel):
    email : str
    password : str

class Token(BaseModel):
    access_token : str 
    token_type : str

class TokenData(BaseModel):
    id : Optional[int] = None


