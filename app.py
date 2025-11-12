from fastapi import FastAPI
import uvicorn
from db.db import init_db
from routes.author_router import router as author_router
from routes.book_router import router as book_router
from routes.user_router import router as user_router

init_db()

app = FastAPI(title="Library Management API")

app.include_router(author_router)
app.include_router(book_router)
app.include_router(user_router)

def start_server():
	uvicorn.run(
		app,
		host="0.0.0.0",
		port=4000,
		log_level="debug",
		reload=True,
	)

if __name__ == "__main__":
	start_server()