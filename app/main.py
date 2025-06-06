from fastapi import FastAPI,Response,status,HTTPException,Request
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
import random


#making fast api instance
class Post(BaseModel):
    title:str
    content:str
    published:bool =  True
    rating: Optional[int] = None

app = FastAPI()
posts = [{"title":"title of post 1","content":"content of post 1","id":1},{"title":"title of post 2","content":"content of post 2","id":2}]

@app.get("/")
async def root():
    return {"message":"this is root"}

#the async keyword is optional, we need it only when we need some asynchronus task
@app.get("/login")
async def read_root():
    return {"Hello": "Welcome to my api"} #fast api automatically converts it into json

# The order of api endpoints does matter

@app.post("/createpost")
def createpost(new_post: Post,response:Response):
    response.status_code = status.HTTP_201_CREATED
    post_dict = new_post.model_dump()
    post_dict["id"] = random.randint(0,1000)
    posts.append(post_dict)
    return {"data":new_post}

def find_post(id):
    for p in posts:
        if p["id"]==id:
            return p
        
@app.get("/posts")
def get_all_post():
    return {"post_detail":posts}

@app.get("/posts/{id}")
def readpost(id:int,response:Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} was not found")
    return {"post_detail":post}

def find_index_post(id):
    for i,p in enumerate(posts):
        if p['id'] == id:
            return i
        
@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def deletepost(id:int,response:Response):
    index = find_index_post(id)
    print(index)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with {id} does not exist")
    posts.pop(index)
    response.status_code = status.HTTP_204_NO_CONTENT
    return response

@app.put("/posts/{id}")
def update_post(id:int,post:Post):
    body = post.model_dump()
    index = find_index_post(id)

    posts[index]["title"] = body["title"]
    posts[index]["content"] = body["content"]

    return {f"Updated post with id {id}"}
    