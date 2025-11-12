from fastapi import FastAPI
from db.db import init_db
from routes.author_router import router as author_router
from routes.book_router import router as book_router

init_db()

app = FastAPI(title="User Management API")

app.include_router(author_router)
app.include_router(book_router)
    