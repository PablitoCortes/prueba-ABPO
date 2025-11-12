from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.db import get_db
from services.books import book_services
from services.exceptions import NotFoundError, BadRequestError
from schemas.book_schema import CreateBookSchema, UpdateBookSchema, BookOut

router = APIRouter(prefix="/books", tags=["Books"])

@router.get("/", response_model=list[BookOut])
def get_books(
    db: Session = Depends(get_db),
    page: int = 1,
    limit: int = 10,
    isAvailable: bool = False,
    title: str = ""
):
	# return list (possibly empty)
	return book_services.get_books(db, page, limit, isAvailable, title)


@router.get("/{id}", response_model=BookOut)
def get_book_by_id(id:int, db:Session = Depends(get_db)):
		book = book_services.get_book_by_id(db, id)
		if not book:
				raise HTTPException(status_code=404, detail="Book not found")
		return book


@router.post("/", response_model=BookOut, status_code=201)
def create_book(data:CreateBookSchema, db:Session = Depends(get_db)):
	# Let Pydantic validate required fields; map service errors to HTTP responses
	try:
		return book_services.create_book(db, data)
	except BadRequestError as e:
		raise HTTPException(status_code=400, detail=str(e))
	except NotFoundError as e:
		raise HTTPException(status_code=404, detail=str(e))
	except Exception:
		raise HTTPException(status_code=500, detail="Internal server error")
		
@router.put("/{id}", response_model=BookOut)
def update_book(id:int, book_data:UpdateBookSchema, db:Session = Depends(get_db)):
	if not book_data:
		raise HTTPException(status_code=400, detail="No data provided for update")
	try:
		updated_book = book_services.update_book(db, id, book_data)
		return updated_book
	except NotFoundError as e:
		raise HTTPException(status_code=404, detail=str(e))
	except BadRequestError as e:
		raise HTTPException(status_code=400, detail=str(e))
	except Exception:
		raise HTTPException(status_code=500, detail="Internal server error")
		
@router.delete("/{id}", status_code=200)
def delete_book(id:int, db:Session = Depends(get_db)):
	try:
		book_services.delete_book(db, id)
		return {"message": "Book deleted successfully"}
	except NotFoundError as e:
		raise HTTPException(status_code=404, detail=str(e))
	except BadRequestError as e:
		raise HTTPException(status_code=400, detail=str(e))
	except Exception:
		raise HTTPException(status_code=500, detail="Internal server error")