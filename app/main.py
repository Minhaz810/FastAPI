from fastapi import FastAPI,Response,status,HTTPException,Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from . import schemas
from . import utils

from . import models
from .database import engine,get_db



models.Base.metadata.create_all(bind=engine)
app = FastAPI()

#getting all posts
@app.get("/posts")
def get_all_posts(db:Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data":posts}

#getting a single post
@app.get("/posts/{id}", status_code=status.HTTP_200_OK, response_model=schemas.PostResponse)
def get_single_post(id:int, db:Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    post = post.first()

    return post


#creating a post
@app.post("/createpost",status_code=status.HTTP_201_CREATED,response_model=schemas.PostResponse)
def create_post(post:schemas.Post,db:Session = Depends(get_db)):
    new_post =  models.Post(**post.model_dump()) #create a new post
    db.add(new_post) #add it to our database
    db.commit() #commit()
    db.refresh(new_post) #stored back into the variable new_post
    return new_post


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
def update_post(post:schemas.Post, id: int, db: Session = Depends(get_db)):
    post_update_query = db.query(models.Post).filter(models.Post.id == id)
    
    if post_update_query.first():
        post_update_query.update(post.model_dump(),synchronize_session=False)
        db.commit()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} does not exist")

    return post_update_query.first()


@app.post("/users",status_code=status.HTTP_201_CREATED,response_model=schemas.UserResponse)
def create_user(user:schemas.UserCreate, db: Session =  Depends(get_db)):
    try:
        #hash the password
        hashed_password = utils.hash(user.password)
        user.password = hashed_password

        #save in db
        new_user = models.User(**user.model_dump())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
@app.get("/users/{id}",response_model=schemas.UserResponse)
def get_user(id:int ,db:Session = Depends(get_db)):
    print(id)
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")
    return user