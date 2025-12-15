
from fastapi import FastAPI, status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils,oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func

router = APIRouter(prefix="/users", tags=["users"])
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserResponse,)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utils.Hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}",response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} was not found",
        )
    return user


@router.get("/{id}/posts", response_model=list[schemas.PostOut])
def get_user_posts(id: int,db: Session = Depends(get_db),current_user: models.User | None = Depends(oauth2.get_current_user_Optional)):
    post_query = (db.query(models.Post,func.count(models.Vote.post_id).label("votes"))
                .join(models.Vote,models.Post.id == models.Vote.post_id,isouter=True).group_by(models.Post.id))

    if current_user and current_user.id == id:
        posts = post_query.filter(models.Post.owner_id == id).all()
    else:
        posts = post_query.filter(
            models.Post.owner_id == id,
            models.Post.published == True
        ).all()
    return posts
@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(db :Session = Depends(get_db),current_user: models.User = Depends(oauth2.get_current_user)):
    user_query = db.query(models.User).filter(models.User.id == current_user.id)
    user_query.delete(synchronize_session=False)
    db.commit()
    return