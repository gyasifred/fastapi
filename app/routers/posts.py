from fastapi import Body, Depends, FastAPI, Response, status, HTTPException, APIRouter
from sqlalchemy import func
from ..import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List, Optional


router = APIRouter(
    prefix="/sqlposts",
    tags=['Posts']
)


# # REGULAR SQL


# @router.get("/posts", response_model=List[schemas.Post])
# def get_post():
#     cursor.execute('''SELECT * FROM posts ''')
#     posts = cursor.fetchall()
#     print(posts)
#     return posts


# # new_posts = ['Ukraine war', 'US intelligence claim the have help sink Russian warship','true'),('funeral', 'I would like you all to know the passing of my grandmother', True),
# #              ('GH Sport'), 'Kotoko wins Ghana PRIMIER LEAGUE', True)]


# @router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
# def create_post(post: schemas.CreatePost):
#     cursor.execute('''INSERT INTO posts (title, content, published)
#      VALUES (%s,%s,%s) RETURNING *''', (post.title, post.content, post.Published))
#     new_post = cursor.fetchone()
#     print(new_post)
#     conn.commit()
#     return new_post


# @ router.get("/posts/{id}", response_model=schemas.Post)
# def get_post(id: int, response: Response):
#     cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
#     post = cursor.fetchone()
#     print(post)
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"post with id {id} not found")
#         # response.status_code = status.HTTP_404_NOT_FOUND
#         # return {"message":f"post with id {id} not found"}

#     return post


# @ router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):
#     cursor.execute(
#         """DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
#     deleted_post = cursor.fetchone()
#     if deleted_post == None:
#         raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,
#                             detail=f"content with id {id} does not exists")
#     conn.commit()
#     return Response(status_code=status.HTTP_204_NO_CONTENT)


# @router.put("/posts/{id}", response_model=schemas.Post)
# def update_post(id: int, post: schemas.CreatePost):
#     cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
#                    (post.title, post.content, post.Published, str(id)))
#     updated_post = cursor.fetchone()
#     if updated_post == None:
#         raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,
#                             detail=f"content with id {id} does not exists")
#     conn.commit()
#     return updated_post

# '''SQLALCHEMY'''


@router.get("/", response_model=List[schemas.PostOut])
def get_post(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    #post = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    #post = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.CreatePost, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # print(current_user.email)
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    #post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authourize")
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,
                            detail=f"content with id {id} does not exists")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authourize to delete post")

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.CreatePost, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_1 = post_query.first()
    if post_1 == None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,
                            detail=f"content with id {id} does not exists")
    if post_1.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authourize to update post")

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
