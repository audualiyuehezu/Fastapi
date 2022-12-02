from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [{"title":"title of post1","content":"This is the content of first title","id":1},
           {"title":"title of post2","content":"This is the content of second title","id":2}
           ]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
         return p

def find_post_index(id):
    for i,p in enumerate(my_posts):
        if p["id"] == id:
            return i


@app.get("/") 
def root():
    return {"This": "Hello world"}

@app.get("/posts")
def get_post():
    return {"data": my_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post:Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0,10000000)
    my_posts.append(post_dict)
    return {"data": post_dict }
#title_str,content_str


@app.get("/posts/{id}")
def get_post(id: int, response:Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND,detail=f"The id: {id} is out of bound ")

        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {f"The id: {id} is out of bound "}"""

    print(post)
    return {"data":post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_post_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Post with id:{id} is not found ")


    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}", status_code=status.HTTP_201_CREATED)
def update_post(id:int, post:Post):
    index = find_post_index(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"The id {id} is not found")
    
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"data": post_dict}