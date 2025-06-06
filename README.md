# FastAPI

## Changing Status Code
__import the status from fastapi__
```bash
from fastapi import FastAPI,status,HTTPException
```
__place status code inside the HTTP Exception or response__(just like DRF)
```bash
response.status_code = status.HTTP_400_BAD_REQUEST
```
or
```bash
raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} was not found")
```

## deletion
__N:B:__ when we are deleting something with the status code 204, then we should not send content back

__important:__

1.If a parameter is in the URL path (/posts/{id}), and you include it in your function with a matching name, FastAPI treats it as a path parameter.

```bash
@app.get("/posts/{id}")
def get_post(id: int):  # <- FastAPI knows `id` comes from path
    return {"id": id}
```

2. Any parameter with a simple type (str, int, bool, etc.) not in the path is treated as a query parameter.

```bash
@app.get("/search")
def search_posts(query: str):  # <- ?query=example
    return {"search": query}
```

3. If a parameter is a Pydantic model, FastAPI assumes it comes from the JSON body.

```bash
from pydantic import BaseModel

class Post(BaseModel):
    title: str
    content: str

@app.post("/posts")
def create_post(post: Post):  # <- From body
    return post
```

4. Use Form(), Header(), Cookie(), etc., from fastapi to tell FastAPI how to extract the data.Use Form(), Header(), Cookie(), etc., from fastapi to tell FastAPI how to extract the data.

```bash
from fastapi import Form

@app.post("/login")
def login(username: str = Form(), password: str = Form()):
    return {"user": username}
```

```bash
from fastapi import FastAPI, Header

app = FastAPI()

@app.get("/items/")
def read_items(user_agent: str = Header(default=None)):
    return {"User-Agent": user_agent}
```
