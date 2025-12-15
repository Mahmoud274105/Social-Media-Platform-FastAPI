from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from .. import models, schemas
import app.oauth2 as oauth2
from typing import Optional
from ..database import get_db
from typing import List
from sqlalchemy import func
from sqlalchemy.orm import Session
router = APIRouter(prefix="/posts",tags=["posts"])

@router.get("/", response_model=list[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), limit:int = 10, skip: int = 0, search: Optional[str] = ""):
    posts = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Post.id == models.Vote.post_id, isouter = True).group_by(models.Post.id).filter(
            models.Post.title.contains(search), models.Post.published == True).limit(limit).offset(skip).all()
    return posts

@router.get("/latest", response_model=schemas.PostOut)
def get_latest_post(db: Session = Depends(get_db)):
    post = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Post.id == models.Vote.post_id, isouter = True).group_by(models.Post.id).filter(models.Post.published == True).order_by(models.Post.created_at.desc()).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="There are no recent posts",
        )
    return post
@router.get("/{id}", response_model=schemas.PostOut)
def get_post_by_id(id: int,db: Session = Depends(get_db),current_user: models.User | None = Depends(oauth2.get_current_user_Optional)):
    post = (
        db.query(
            models.Post,
            func.count(models.Vote.post_id).label("votes")
        )
        .join(
            models.Vote,
            models.Post.id == models.Vote.post_id,
            isouter=True
        )
        .group_by(models.Post.id)
        .filter(models.Post.id == id)
        .first()
    )

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} was not found",
        )

    if not post.Post.published:
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Login required to view this post",
            )

        if post.Post.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view this post",
            )

    return post



@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.PostResponse,
)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db),current_user: models.User = Depends(oauth2.get_current_user)):
    new_post = models.Post(**post.dict())
    new_post.owner_id = current_user.id
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),current_user: models.User = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} was not found",
        )

    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )

    post_query.delete(synchronize_session=False)
    db.commit()
    return


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, updated_post: schemas.PostUpdate, db: Session = Depends(get_db),current_user: models.User = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} was not found",
        )
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()