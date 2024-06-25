from fastapi import FastAPI,Response,status,HTTPException
from pydantic import BaseModel
from typing import Optional
from random import randrange
import time
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="fastapi",
            user="postgres",
            password="root",
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        print("database connection was successfully established")
        break
    except Exception as e:
        print("Failed to connect to database ")
        print("details:",e)
        time.sleep(2)

        

def find_post(id:int):
    for post in my_posts:
        if post["id"] == id:
            return post
        
def find_index(id:int):
    for i,p in enumerate(my_posts):
        if p["id"] == id:
            return i
   

my_posts = [
    {'title': "title of post 1", "content": "content of post 1", "id": 1},
    {'title': "favorite foods", "content": "i like pizza", "id": 2}
]

@app.get("/")
async def root():
    return {"message": "welcome to my ai"}

@app.get("/posts")
async def get_post():
    cursor.execute("SELECT * FROM posts")
    post = cursor.fetchall()
    return {"data": post}

@app.post("/post")
async def create_post(post: Post,status_code = status.HTTP_201_CREATED):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
               (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    
    conn.commit()
    return {"data": new_post}


@app.get("/posts/{id}")
async def get_post(id:int,response :Response):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""",(str(id)))
    test_post = cursor.fetchone()
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post {id} not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message": "post not found"}

    return {"post details":test_post}


@app.delete("/posts/{id}")
async def delete_post(id:int,status_code = status.HTTP_204_NO_CONTENT):
    index = find_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post {id} not exist")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message": "post not found"}
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@app.put("/posts/{id}")
async def update_post(id:int,post:Post):
    index = find_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post {id} not exist")
    post_dict = post.dict()
    post_dict[id] = id
    my_posts[index] = post_dict

    print(post)
    return {"message":"post updated"}
