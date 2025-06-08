# Here we will have all the pydantic/schema models
from pydantic import BaseModel,EmailStr
from typing import Optional
from datetime import datetime

class Post(BaseModel):
    title:str
    content:str
    published:bool = True

class CreatePost(BaseModel):
    title:str
    content:str
    published:bool = True

class UpdatePost(BaseModel):
    published:bool #if the user is have the permission to update this published field only

class PostResponse(BaseModel):
    id:int
    title:str
    content:str
    published:bool
    create_at:datetime

    class Config:
        from_attributes = True

"""
or we can do 
class PostBase(BaseModel):
    title:str
    content:str
    published:bool = True

class CreatePost(PostBase):
    pass

class UpdatePost(BaseModel):
    published: bool #if the user is have the permission to update this published field only

"""

class UserCreate(BaseModel):
    email:EmailStr
    password:str

class UserResponse(BaseModel):
    id:int
    email:EmailStr

    class Config:
        from_attributes = True