from .. import models,schemas,utils
from fastapi import FastAPI,status,HTTPException,Response,Depends,APIRouter
from sqlalchemy.orm import Session
from .. database import get_db

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)
#getting all posts
@router.get("/")
def get_all_posts(db:Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data":posts}

#getting a single post
@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.PostResponse)
def get_single_post(id:int, db:Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    post = post.first()

    return post


#creating a post
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.PostResponse)
def create_post(post:schemas.Post,db:Session = Depends(get_db)):
    new_post =  models.Post(**post.model_dump()) #create a new post
    db.add(new_post) #add it to our database
    db.commit() #commit()
    db.refresh(new_post) #stored back into the variable new_post
    return new_post


#deleting a post
@router.delete("/{id}")
def delete_post(id: int, db: Session = Depends(get_db)):
    post_delete_query = db.query(models.Post).filter(models.Post.id == id)
    
    if post_delete_query.first():
        post_delete_query.delete(synchronize_session=False)
        db.commit()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} does not exist")

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}")
def update_post(post:schemas.Post, id: int, db: Session = Depends(get_db)):
    post_update_query = db.query(models.Post).filter(models.Post.id == id)
    
    if post_update_query.first():
        post_update_query.update(post.model_dump(),synchronize_session=False)
        db.commit()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} does not exist")

    return post_update_query.first()