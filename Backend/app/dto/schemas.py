from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class ShowUser(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True

class User(BaseModel):
    name: str
    email: str
class ArticleBase(BaseModel):
    title: str
    content: str


class ArticleCreate(ArticleBase):
    pass

class Article(ArticleBase):
    id: int
    created_at: datetime  # Include created_at in the response schema

    class Config:
        orm_mode = True