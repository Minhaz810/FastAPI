# Here we will have all the pydantic/schema models
from pydantic import BaseModel
from typing import Optional

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