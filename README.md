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

__Question:__ When using request.body() or request.json() directly inside my FastAPI endpoint function, why do I need to declare the function as async def and use await?
But when I use a Pydantic model as a parameter, I don't need to use async/await in my function even though the request body is still being read asynchronously. Why is that?

__Ans:__ 
```bash
When you use request.body() or request.json() directly inside your function, these methods are asynchronous and return coroutines that must be awaited. This means your function must be declared as async def so you can use await to properly read the request body without blocking. If you don’t use async def and await, Python will raise an error because you cannot await inside a synchronous function.

In contrast, when you use a Pydantic model as a parameter in your endpoint function, FastAPI automatically handles the asynchronous reading and parsing of the request body before your function is called. FastAPI awaits the request body reading and JSON parsing internally, validates the data with Pydantic, and then passes the fully parsed and validated model instance to your function. By the time your function runs, all the asynchronous operations have already completed, so you don’t need to use async/await in your function just to access the parsed data.

```
