from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr

class PostBase(BaseModel):
    title: str
    content: str
    publish: bool = True

class PostCreate(PostBase):
    pass

class CreateUserPost(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Post(PostBase):
    id: int
    owner_id: int
    created_at: datetime
    owner_id: CreateUserPost
    
    model_config = ConfigDict(from_attributes=True)

class PostResponse(Post):
    pass   
 
    model_config = ConfigDict(from_attributes=True)


class CreateUser(BaseModel):
    email: EmailStr
    password : str



class UserLogin(CreateUser):
    pass


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None