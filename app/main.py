from fastapi import FastAPI,Response,status,HTTPException,Request,Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
import random
from sqlalchemy.orm import Session


from . import models
from .database import engine,get_db

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

class Post(BaseModel):
    title:str
    content:str
    published:bool = True


#getting all posts
@app.get("/posts")
def get_all_posts(db:Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data":posts}

#getting a single post
@app.get("/posts/{id}")
def get_single_post(id:int, db:Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    post = post.first()

    return {"data":post}


#creating a post
@app.post("/createpost")
def create_post(post:Post,db:Session = Depends(get_db)):
    new_post =  models.Post(**post.model_dump()) #create a new post
    db.add(new_post) #add it to our database
    db.commit() #commit()
    db.refresh(new_post) #stored back into the variable new_post
    return {"data":new_post}


#deleting a post
@app.delete("/posts/{id}")
def delete_post(id: int, db: Session = Depends(get_db)):
    post_delete_query = db.query(models.Post).filter(models.Post.id == id)
    
    if post_delete_query.first():
        post_delete_query.delete(synchronize_session=False)
        db.commit()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} does not exist")

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(post:Post, id: int, db: Session = Depends(get_db)):
    post_update_query = db.query(models.Post).filter(models.Post.id == id)
    
    if post_update_query.first():
        post_update_query.update(post.model_dump(),synchronize_session=False)
        db.commit()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} does not exist")

    return {"data":post_update_query.first()}