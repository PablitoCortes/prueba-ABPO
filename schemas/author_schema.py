from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UpdateAuthorSchema(BaseModel):
	name: Optional[str] = None
	nationality: Optional[str] = None
	date_of_birth: Optional[str] = None


class CreateAuthorSchema(BaseModel):
	name: str
	nationality: Optional[str] = None
	date_of_birth: Optional[str] = None

class AuthorOut(BaseModel):
	model_config = {"from_attributes": True}
	
	id: int
	name: str
	nationality: Optional[str] = None
	date_of_birth: Optional[str] = None
	created_at: datetime
	updated_at: datetime