import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from db.db import Base, get_db
from app import app

# Importar todos los modelos para que se registren en Base
from models.author_model import Author
from models.book_model import Book
from models.user_model import User

# Base de datos en memoria para tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Crea una nueva base de datos para cada test"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Crea un cliente de prueba con base de datos override"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def test_user_token(client, db_session):
    """Crea un usuario de prueba y retorna su token"""
    user_data = {
        "username": "testuser",
        "password": "testpass123"
    }
    # Registrar usuario
    response = client.post("/api/users/register", json=user_data)
    assert response.status_code in [200, 201], f"Error registrando usuario: {response.text}"
    # Hacer login
    response = client.post("/api/users/login", json=user_data)
    assert response.status_code == 200, f"Error en login: {response.text}"
    return response.json()["access_token"]

