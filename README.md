# Authors & Books API

Small FastAPI project using SQLAlchemy and SQLite to manage authors and books.

This README contains clear installation and run instructions for Windows (PowerShell) plus useful tips for development.

---

## Requirements

- Python 3.10+ (recommended)
- Git (optional)

The project uses these Python libraries (see `requirements.txt`):
- fastapi
- uvicorn
- sqlalchemy
- pydantic

---

## Setup (Windows PowerShell)

Open PowerShell in the project root (where `app.py` is located) and run:

1. Create a virtual environment

```powershell
python -m venv venv
```

2. Activate the virtual environment

```powershell
# PowerShell
.\venv\Scripts\Activate.ps1
# or (legacy)
# .\venv\Scripts\activate
```

3. Install dependencies

```powershell
pip install -r requirements.txt
```

(If you add new dependencies, update `requirements.txt` with `pip freeze > requirements.txt`.)

---

## Run the application (development)

Start the FastAPI app with uvicorn (reload enabled for development):

```powershell
uvicorn app:app --reload --port 8000
```

- The application will be available at: http://127.0.0.1:8000
- Interactive OpenAPI docs: http://127.0.0.1:8000/docs

Notes:
- The project uses an SQLite file named `autor.db` at the project root by default.
- On app startup the code calls the DB initialization function which will create tables if they don't exist.

---

## Project structure (important files)

- `app.py` — FastAPI application entry point (includes routers and initializes DB)
- `db/db.py` — SQLAlchemy engine, SessionLocal, Base and `init_db()` helper
- `models/` — SQLAlchemy models (`author_model.py`, `book_model.py`)
- `crud/` — database access functions (create/get/update/delete)
- `routes/` — FastAPI routers (e.g. `author_router.py`, `book_router.py`)
- `schemas/` — Pydantic models for request/response validation
- `requirements.txt` — Python dependencies

---

## Database notes

- The project uses SQLite (`autor.db`). By default `init_db()` (called on startup) runs `Base.metadata.create_all(bind=engine)` to create tables.
- Development workflow:
  - If you change models and are OK losing dev data, you can delete `autor.db` and restart the app to recreate tables.
  - To preserve data across schema changes in a controlled way, use Alembic for migrations (recommended for staging/production).

Quick commands (PowerShell):

```powershell
# backup existing DB
Copy-Item .\autor.db .\autor.db.bak

# remove DB (will cause tables to be recreated on next app start)
Remove-Item .\autor.db
```

---

## Minimal API usage examples (PowerShell / curl style)

1) Create an author (POST /autors/)

```powershell
curl.exe -X POST "http://127.0.0.1:8000/autors/" -H "Content-Type: application/json" -d '{"name":"Gabriel García Márquez","nationality":"Colombian","dob":"1927-03-06"}'
```

Response: 201 Created with the created author JSON (including `id`).

2) Create a book (POST /books/)

- First ensure you have an author (note the id from the previous response, e.g. `1`).

```powershell
curl.exe -X POST "http://127.0.0.1:8000/books/" -H "Content-Type: application/json" -d '{"title":"One Hundred Years of Solitude","isbn":"9780060883287","author_id":1}'
```

Response: 201 Created with the created book JSON.

3) Retrieve books and authors

- GET all authors: `GET /autors/`
- GET author by id: `GET /autors/{id}`
- GET all books: `GET /books/`
- GET book by id: `GET /books/{id}`

Open the docs for an interactive UI: http://127.0.0.1:8000/docs

---

## Error handling expectations

The API follows these response semantics:

- 200 OK — successful GET/PUT/DELETE operations
- 201 Created — successful POST (resource created)
- 400 Bad Request — client-provided data is invalid (routes may return 422 when Pydantic validation fails)
- 404 Not Found — requested resource does not exist (e.g. `author_id` not found)
- 500 Internal Server Error — unhandled exceptions or response validation failures

If you see `ResponseValidationError` in logs, it usually means the `response_model` declared in a route does not match the value returned by the route. Make sure response models have `orm_mode = True` when returning SQLAlchemy objects.

---

## Development tips

- Keep request and response Pydantic models separate. Use `CreateXxx` for incoming data and `XxxOut` for responses.
- Use `orm_mode = True` in response models to allow Pydantic to read SQLAlchemy attributes.
- Keep `crud/` functions focused on DB operations and avoid returning HTTP responses from the crud layer; return data and let routers convert to responses and status codes.

---

## Optional: Using Alembic (migrations)

For non-destructive schema changes (recommended for production):

1. Install alembic in the venv:

```powershell
pip install alembic
```

2. Initialize Alembic (one-time):

```powershell
alembic init alembic
```

3. Configure `alembic/env.py` to expose your SQLAlchemy `Base.metadata` (import your models module so mappers are registered), then generate and apply migrations:

```powershell
alembic revision --autogenerate -m "Describe changes"
alembic upgrade head
```

---

## Troubleshooting common issues

- ImportError about `Session` from sqlalchemy: import `Session` from `sqlalchemy.orm` (not from `sqlalchemy`).
- `TypeError: 'author_id' is an invalid keyword argument for Book`: verify the column name in `models/book_model.py` matches the keyword you pass when creating a `Book` instance (`author_id` vs `autor_id`).
- `sqlite3.OperationalError: table books has no column named author_id`: your DB file was created before the model change — either migrate schema or recreate DB.
- `ResponseValidationError`: make sure response models match returned objects and enable `orm_mode = True`.

---

## Contributing

Small project. If you make changes:
- Run and test endpoints locally.
- Add or update Pydantic schemas when models change.
- Consider Alembic migration scripts for schema updates.

---

If you want, I can also:
- add a `scripts/reset_db.py` to quickly recreate the database,
- add an `examples/` folder with tiny test scripts, or
- create a basic `Makefile` / PowerShell script with common tasks.

Tell me which of those you'd like next.
