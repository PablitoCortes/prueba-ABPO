from pydantic import BaseModel
from typing import List, Optional

from models.book_model import Book


class UpdateAuthorSchema(BaseModel):
	name: Optional[str] = None
	nationality: Optional[str] = None
	dob: Optional[str] = None

class CreateAuthorSchema(BaseModel):
	name: str
	nationality: Optional[str] = None
	dob: Optional[str] = None

class BaseAuthorSchema(BaseModel):
	id: int
	name: str
	nationality: Optional[str] = None
	dob: Optional[str] = None

	class Config:
		orm_mode = True