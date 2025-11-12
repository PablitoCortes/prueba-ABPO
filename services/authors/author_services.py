from sqlalchemy.orm import Session
from datetime import datetime
from models.author_model import Author
from schemas.author_schema import CreateAuthorSchema, UpdateAuthorSchema
from services.exceptions import NotFoundError, BadRequestError


def create_author(db: Session, data: CreateAuthorSchema):
    if not data.name:
        raise BadRequestError("Name is required to create an author")

    new_author = Author(
        name=data.name,
        nationality=data.nationality,
        date_of_birth=data.date_of_birth)

    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    return new_author


def get_authors(db: Session):
    return db.query(Author).all()


def get_author_by_id(db: Session, author_id: int):
    return db.query(Author).filter(Author.id == author_id).first()


def update_author(db: Session, id: int, author_data: UpdateAuthorSchema):
    found_author = db.query(Author).filter(Author.id == id).first()
    if not found_author:
        raise NotFoundError("Author not found")

    for field, value in author_data.model_dump(exclude_unset=True).items():
        setattr(found_author, field, value)
    found_author.updated_at = datetime.now()
    db.commit()
    db.refresh(found_author)
    return found_author


def delete_author(db: Session, author_id: int):
    found_author = db.query(Author).filter(Author.id == author_id).first()
    if not found_author:
        raise NotFoundError("Author not found")

    if found_author.books:
        raise BadRequestError("Cannot delete this author; books are associated")

    db.delete(found_author)
    db.commit()
    return found_author
