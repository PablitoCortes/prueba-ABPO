from pydantic import BaseModel
from typing import Optional
from datetime import date

class UpdateAuthorSchema(BaseModel):
	name: Optional[str] = None
	nationality: Optional[str] = None
	date_of_birth: Optional[str] = None


class CreateAuthorSchema(BaseModel):
	name: str
	nationality: Optional[str] = None
	date_of_birth: Optional[str] = None

class AuthorOut(BaseModel):
	id: int
	name: str
	nationality: Optional[str] = None
	date_of_birth: Optional[str] = None
	created_at: date
	updated_at: date

	class Config:
		orm_mode = True