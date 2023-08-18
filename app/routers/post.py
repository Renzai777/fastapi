from .. import models, schemas
from fastapi import FastAPI , Response, status , HTTPException , Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import  get_db
from typing import List, Optional
from .. import oauth2
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags =["Posts"]
)



@router.get("/", response_model=List[schemas.PostOut])
# @router.get("/")
def get_posts(db: Session = Depends(get_db), current_user: int= Depends(oauth2.get_current_user),limit: int = 10, skip: int=0, search: Optional[str]=""):

    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()
    # print(posts)
    print(limit)
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts

# @app.post("/createposts")
# def create_post(payload: dict = Body(...)):
#     print(payload)
#     return {"new_post": f"title: {payload['title']}  content: {payload['content']}"}

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post:schemas.PostCreate,db: Session = Depends(get_db), current_user: int= Depends(oauth2.get_current_user)):
    # print(post)
    # print(post.dict())
    # post_dict = post.dict()
    # post_dict['id'] = randrange(0,1000000000000000)
    # my_posts.append(post_dict)
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content ,post.published))
    # new_post = cursor.fetchone()
    # #After inserting data it needs to be commited
    # conn.commit()
    print(post.dict())
    # print(current_user.email)
    # print(current_user.id)
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    new_post = models.Post(owner_id=current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id : int, db: Session = Depends(get_db), current_user: int= Depends(oauth2.get_current_user)):
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id)))
    # post = cursor.fetchone()
    # print(test_post)
    # print(id,type(id))
    # post = find_post(id)
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    print(post)

    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id {id} was not found"}

        # response.status_code = 404

    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int , db: Session = Depends(get_db),current_user: int= Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)) )
    # deleted_post = cursor.fetchone()
    # conn.commit()
    # index = find_index_post(id)
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post wih id: {id} does not exist")
    # my_posts.pop(index)
    if post.owner_id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    post_query.delete(synchronize_session = False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    # return {"message" : "Post was successfully daleted"}


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, upated_post: schemas.PostCreate, db: Session = Depends(get_db),current_user: int= Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s ,published = %s WHERE id = %s RETURNING * """, (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    # index = find_index_post(id)
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    if post.owner_id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    # post_dict = post.dict()
    # post_dict['id'] = id
    # my_posts[index] = post_dict
    post_query.update(upated_post.dict(),synchronize_session = False)
    db.commit()
    return post_query.first()


