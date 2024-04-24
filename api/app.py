from fastapi import FastAPI
import uvicorn
from schema import *
from database import session
import requests
from config import SERVER_BASE_URL
from sqlalchemy.sql import desc

description = """
Content Management System API 

## Items

You can fetch data in different formats.
All the blogs published in the webiste will be available
"""

app = FastAPI(
    title="MyMedium",
    description=description,
    summary="All the content on single request",
    version="0.0.1",
)

def get_img_address(post_id):
    # url = SERVER_BASE_URL+'/post/image/address/'
    # myobj = {'post': post_id}
    # res = requests.post(url, json = myobj)
    # print(res.status_code)
    query = session.query(Post).filter( Post.id == post_id)
    result = query.all()
    posts = []
    for  post in result:
        return SERVER_BASE_URL+'/media/'+post.image
    #return SERVER_BASE_URL+res.json()['url']

@app.get("/posts")
def get_all_posts():
    query = session.query(User, Post).filter(User.email == Post.user_id).order_by(desc(Post.updated))
    result = query.all()
    posts = []
    for user, post in result:
        print(f"User: {user.email}, Post content: {post.image}")
        img_url = get_img_address(post.id)
        posts.append({
            "id" : post.id,
            "title": post.title,
            "subheading": post.subheading,
            "tag": post.tag,
            "image" : img_url
        })
    return {"status":"success","posts": posts}


@app.get("/author/posts/{author}")
def get_author_posts(author: str):
    query = session.query(User, Post).filter(User.email == Post.user_id, User.email==author).order_by(desc(Post.updated))
    result = query.all()
    posts = []
    for user, post in result:
        print(f"User: {user.email}, Post content: {post.image}")
        img_url = get_img_address(post.id)
        posts.append({
            "id" : post.id,
            "title": post.title,
            "subheading": post.subheading,
            "tag": post.tag,
            "image" : img_url
        })
    return {"status":"success","posts": posts}

@app.get("/author/{author}")
def get_author(author: str):
    query = session.query(User).filter(User.email==author)
    result = query.all()
    authors = []
    for user in result:
        authors.append({
            "email" : user.email,
            "name" : user.name
        })
    if len(authors) == 1:
        return {"status":"success","author": authors[0]}
    else:
        return {"status":"failure"}

@app.get("/tag/posts/{tag}")
def get_tag_posts(tag: str):
    query = session.query(Post).filter(Post.tag == tag.capitalize())
    result = query.all()
    posts = []
    for post in result:
        img_url = get_img_address(post.id)
        posts.append({
            "id" : post.id,
            "title": post.title,
            "subheading": post.subheading,
            "tag": post.tag,
            "image" : img_url
        })
    return {"status":"success","posts": posts}


@app.get("/post/{id}")
def get_post_details(id: int):
    query = session.query(User, Post).filter(User.email == Post.user_id, Post.id == id)
    result = query.all()
    posts = []
    for user, post in result:
        print(f"User: {user.email}, Post content: {post.image}")
        img_url = get_img_address(post.id)
        posts.append({
            "id" : id,
            "title": post.title,
            "subheading": post.subheading,
            "tag": post.tag,
            "image" : img_url,
            "content" : post.content,
            "author" : user.email
        })
    if len(posts) == 1:
        return {"status":"success","post": posts[0]}
    else:
        return {"status":"failure"}
        
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8081)