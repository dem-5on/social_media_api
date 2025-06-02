from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from .. import database, models, utils, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=['authentication'])

@router.post('/login')
def login(user_auth: OAuth2PasswordRequestForm= Depends(),db: Session= Depends(database.get_db)):
    user = db.query(models.Users).filter(models.Users.email == user_auth.username).first()

    #check if user exist on database
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid credentials')
    
    #compare password on database and password input by user
    if not utils.verify(user_auth.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid credentials')
    
    #creat token
    access_token = oauth2.create_access_token(data= {"user_id": user.id})
    return {
        'access token': access_token,
        "token type": "bearer"
    }