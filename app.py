from fastapi import FastAPI, APIRouter
import uvicorn
from db.db import init_db
from routes.author_router import router as author_router
from routes.book_router import router as book_router
from routes.user_router import router as user_router

init_db()

app = FastAPI(title="Library Management API")

# Router principal con prefijo /api
api_router = APIRouter(prefix="/api")

# Incluir todos los routers en el router principal
api_router.include_router(author_router)
api_router.include_router(book_router)
api_router.include_router(user_router)

# Incluir el router principal en la app
app.include_router(api_router)

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