from typing import List, Optional
from fastapi import Depends, HTTPException, Response, status, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(
    prefix= '/posts',
    tags= ['Posts']
)


#CRUD ---- FUNCTIONALITY AND THIS PART IS THE CREATE(C)
@router.post('/', status_code=status.HTTP_201_CREATED, response_model= schemas.PostResponse)
def creat_post(post: schemas.PostCreate, db : Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    my_posts = models.Posts(owner_id=current_user.id,**post.dict())
    db.add(my_posts)
    db.commit()
    db.refresh(my_posts)

    return my_posts


#CRUD ---- FUNCTIONALITY AND THIS PART IS THE UPDATE(U)
@router.put("/{id}",  response_model = schemas.PostCreate)
def update_post(id: int, post: schemas.PostCreate, db : Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    update_post = db.query(models.Posts).filter(models.Posts.id == id)
    existing_post = update_post.first()
    if existing_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")
    
    if existing_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized to update this post")    
    
    update_post.update(post.dict(), synchronize_session=False)
    db.commit()
    return  update_post.first()


#CRUD ---- FUNCTIONALITY AND THIS PART IS THE READ(R)
@router.get('/posts',  response_model = List[schemas.PostBase])
def get_all(db : Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
             limit=10, skip: int =0, search: Optional[str]= ""):
    
    post = db.query(models.Posts).filter(models.Posts.title.contains(search)).limit(limit).offset(skip).all()
    if post == None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return  post


#CRUD ---- FUNCTIONALITY AND THIS PART IS THE READ(R)
@router.get('/{id}',  response_model = schemas.PostBase)
def get_posts(id: int, db : Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Posts).filter(models.Posts.id == id).first()
    if post == None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return  post


#CRUD ---- FUNCTIONALITY AND THIS PART IS THE DELETE(D)
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db : Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Posts).filter(models.Posts.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized to update this post")    
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

