from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


@app.get("/") 
def root():
    return {"This": "Hello world"}

@app.get("/posts")
def get_post():
    return {"Foods":"Food is the best thing on earth to eat"}

@app.post("/posts")
def create_posts(post:Post):
    print(post)
    print(post.dict())  
    return {"data": post }
#title_str,content_str