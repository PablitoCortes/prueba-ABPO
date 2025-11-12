from pydantic import BaseModel
from typing import Optional

class UpdateAuthorSchema(BaseModel):
	name: Optional[str] = None
	nationality: Optional[str] = None
	date_of_birth: Optional[str] = None


class CreateAuthorSchema(BaseModel):
	name: str
	nationality: Optional[str] = None
	date_of_birth: Optional[str] = None

class BaseAuthorSchema(BaseModel):
	id: int
	name: str
	nationality: Optional[str] = None
	date_of_birth: Optional[str] = None

	class Config:
		orm_mode = True