from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [
    {'title': "title of post 1", "content": "content of post 1", "id": 1},
    {'title': "favorite foods", "content": "i like pizza", "id": 2}
]

@app.get("/")
async def root():
    return {"message": "welcome to my ai"}

@app.get("/post")
async def get_post():
    return {"data": my_posts}

@app.post("/post")
async def create_post(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 10000)
    my_posts.append(post_dict)
    return {"data": post_dict}
