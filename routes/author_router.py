from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.db import get_db
from services.authors import author_services
from services.exceptions import NotFoundError, BadRequestError
from schemas.author_schema import AuthorOut, CreateAuthorSchema, UpdateAuthorSchema
from core.auth import get_current_user

router = APIRouter(prefix="/authors", tags=["Authors"])

@router.get("/", response_model=list[AuthorOut])
def get_authors(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    authors = author_services.get_authors(db)
    return authors


@router.get("/{id}", response_model=AuthorOut)
def get_author_by_id(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    author = author_services.get_author_by_id(db, id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@router.post("/", response_model=AuthorOut, status_code=201)
def create_author(
    data: CreateAuthorSchema,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        return author_services.create_author(db, data)
    except BadRequestError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.put("/{id}", response_model=AuthorOut)
def update_author(
    id: int,
    author_data: UpdateAuthorSchema,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if not author_data:
        raise HTTPException(status_code=400, detail="No data provided for update")
    try:
        updated_author = author_services.update_author(db, id, author_data)
        return updated_author
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except BadRequestError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/{id}", status_code=200)
def delete_author(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    try:
        author_services.delete_author(db, id)
        return {"message": "Author deleted successfully"}
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except BadRequestError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")
