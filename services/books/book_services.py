from sqlalchemy.orm import Session, joinedload
from models.book_model import Book
from models.author_model import Author
from schemas.book_schema import CreateBookSchema, UpdateBookSchema
from services.exceptions import NotFoundError, BadRequestError

def create_book(db: Session, data: CreateBookSchema):

	if not data.title or not data.author_id or not data.isbn:
		raise BadRequestError("Missing data to create a book")

	found_author = db.query(Author).filter(Author.id == data.author_id).first()

	if not found_author:
		raise NotFoundError("Author not found")

	existing_book = db.query(Book).filter(Book.isbn == data.isbn).first()

	if existing_book:
		raise BadRequestError("A book with this ISBN already exists")

	new_book = Book(
		title=data.title,
		isbn=data.isbn,
		author_id=data.author_id,
		genre=data.genre,
		published_year=data.published_year,
		is_available=data.isAvailable,
	)

	db.add(new_book)
	db.commit()
	db.refresh(new_book)
	return new_book

def get_books(db: Session, page: int = 1, limit: int = 10, isAvailable: bool = False, title: str = ""):
    skip = (page - 1) * limit
    query = db.query(Book).options(joinedload(Book.author))

    if isAvailable:
        query = query.filter(Book.is_available == True)
    
    if title:
        query = query.filter(Book.title.ilike(f"%{title}%"))

    return query.offset(skip).limit(limit).all()


def get_book_by_id(db: Session, book_id: int):
    return db.query(Book).options(joinedload(Book.author)).filter(Book.id == book_id).first()


def update_book(db: Session, id: int, book_data: UpdateBookSchema):
	found_book = db.query(Book).filter(Book.id == id).first()
	if not found_book:
		raise NotFoundError("Book not found")
	if book_data.author_id:
		found_author = db.query(Author).filter(Author.id == book_data.author_id).first()
		if not found_author:
			raise NotFoundError("Author not found")

	for field, value in book_data.model_dump(exclude_unset=True).items():
		if field == "isAvailable":
			setattr(found_book, "is_available", value)
		else:
			setattr(found_book, field, value)

	db.commit()
	db.refresh(found_book)
	return found_book



def delete_book(db: Session, book_id: int):
	found_book = db.query(Book).filter(Book.id == book_id).first()
	if not found_book:
		raise NotFoundError("Book not found")

	db.delete(found_book)
	db.commit()
	return found_book