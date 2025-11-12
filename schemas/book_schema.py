from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from schemas.author_schema import AuthorOut

class CreateBookSchema(BaseModel):
    title: str
    isbn: str
    author_id: int  
    published_year: Optional[int] = None
    genre: Optional[str] = None
    isAvailable: bool = True

class UpdateBookSchema(BaseModel):
    title: Optional[str] = None
    isbn: Optional[str] = None
    author_id: Optional[int] = None
    published_year: Optional[int] = None
    genre: Optional[str] = None
    isAvailable: Optional[bool] = None

class BookOut(BaseModel):
    id: int
    title: str
    isbn: str
    author: AuthorOut 
    published_year: Optional[int] = None
    genre: Optional[str] = None
    is_available: bool = True
    created_at: datetime
    updated_at: datetime
	
    class Config:
        orm_mode = True