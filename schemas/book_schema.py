from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from schemas.author_schema import BaseAuthorSchema

class CreateBookSchema(BaseModel):
    title: str
    isbn: str
    author_id: int  
    published_date: Optional[datetime] = None
    genre: Optional[str] = None
    isAvailable: bool = True

class UpdateBookSchema(BaseModel):
    title: Optional[str] = None
    isbn: Optional[str] = None
    author_id: Optional[int] = None
    published_date: Optional[datetime] = None
    genre: Optional[str] = None
    isAvailable: Optional[bool] = None

class BookOut(BaseModel):
    id: int
    title: str
    isbn: str
    author: BaseAuthorSchema 
    published_date: Optional[datetime] = None
    genre: Optional[str] = None
    isAvailable: bool = True

    class Config:
        orm_mode = True