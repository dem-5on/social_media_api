from typing import List
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get('/', response_model = List[schemas.PostBase])
def root(db : Session = Depends(get_db)):
    posts = db.query(models.Posts).all()
    return posts


