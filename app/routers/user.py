
from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(
    prefix= '/users',
    tags= ['Users']
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.CreateUserPost)
def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):

    # Check if user exists
    existing_user = db.query(models.Users).filter(models.Users.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with email: {user.email} already exists"
        )

    #hashing password
    hashed = utils.hash(user.password)
    user.password = hashed

    new_user = models.Users(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get('/{id}', response_model=schemas.CreateUserPost)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, details=f"User with id: {id} not found")
    return user