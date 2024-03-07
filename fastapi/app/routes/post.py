from fastapi import FastAPI, HTTPException, Response, status, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix = "/posts",
    tags=['Posts']
)


@router.get("/")
def get_post(db : Session = Depends(get_db), response_model=List[schemas.Post]):
    posts = db.query(models.Post).all()
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post : schemas.PostCreate, db : Session = Depends(get_db),):
    
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post

@router.get("/{id}")
def get_post(id: int, response: Response, db : Session = Depends(get_db), response_model=schemas.Post):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
    return post





@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db : Session = Depends(get_db), response_model=schemas.Post):
    post = db.query(models.Post).filter(models.Post.id == id)
    
    if post.first() == None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                           detail=f"post with id: {id} was not found") 
    post.delete(synchronize_session=False)
    db.commit()
   
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put("/{id}")
def update_post(id: int, post: schemas.PostCreate, db : Session = Depends(get_db), response_model=schemas.Post):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    older_post = post_query.first()
    
    if older_post == None:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                           detail=f"post with id: {id} was not found")
    post_query.update(post.dict(), synchronize_session=False)
    
    db.commit()
    
    return post_query.first()
