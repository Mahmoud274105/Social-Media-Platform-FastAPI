from datetime import datetime
from pydantic import BaseModel, EmailStr
#from pydantic.types import conint
from typing import Literal

# ---------- POST SCHEMAS ----------


# ---------- USER SCHEMAS ----------

class UserBase(BaseModel):
    name: str
    age: int


class UserCreate(UserBase):
    email: EmailStr
    password: str
    name: str
    age: int
    phone_number: str = None

class UserUpdate(UserBase):
    pass


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    age: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
class UserPostResponse(BaseModel):
    id: int
    name: str
    created_at: datetime
    model_config = {
        "from_attributes": True
    }
        
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner : UserPostResponse
    
    model_config = {
        "from_attributes": True
    }

class PostOut(BaseModel):
    Post: PostResponse
    votes: int
    
    model_config = {
        "from_attributes": True
    }

    
class Token(BaseModel):
    access_token: str
    token_type :str
    model_config = {
        "from_attributes": True
    }

class TokenData(BaseModel):
    id: int | None = None

class Vote(BaseModel):
    post_id: int
    dir: Literal[0, 1]