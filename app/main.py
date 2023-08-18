from fastapi import FastAPI
from .database import engine
from . import models
from .routers import post, user, auth, vote
# models.Base.metadata.create_all(bind=engine)

from fastapi.middleware.cors import CORSMiddleware

# origins = ["https://www.google.com", "https://www.youtube.com"]
origins = ["*"]


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency

#pydantic model defines the structure of a request and response






# my_posts = [{"title": "title of post 1", "content": "content of post 1", "id":1}, {"title": "favorite dog breeds", "content":"rotweiller", "id" : 2}]


# def find_post(id):
#     for p in my_posts:
#         if p["id"] == id:
#             return p
#
#
# def find_index_post(id):
#     for i , p in enumerate(my_posts):
#         if p['id'] == id:
#             return i


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return {"message": "Welcome to my api!!"}

# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):
#     # posts = db.query(models.Post)
#     # print(posts)
#     posts = db.query(models.Post).all()
#     return {"data": "successfull"}






# @app.get("/posts/latest")
# def get_latest_post():
#     post = my_posts[len(my_posts)-1]
#     return {"data":post}

