# Here we will have all the pydantic/schema models
from pydantic import BaseModel,EmailStr
from typing import Optional
from datetime import datetime



class UserCreate(BaseModel):
    email:EmailStr
    password:str

class UserResponse(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email:EmailStr
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id:Optional[int]

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
    created_at:datetime
    user_id:int
    user:UserResponse

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
