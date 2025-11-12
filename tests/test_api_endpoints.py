import pytest
from fastapi.testclient import TestClient
from models.author_model import Author
from models.book_model import Book
from tests.conftest import client, test_user_token, db_session


class TestAuthorEndpoints:
    """Tests para los endpoints de autores"""
    
    def test_get_authors_empty(self, client: TestClient, test_user_token: str):
        """Test: GET /api/authors/ con lista vacía"""
        response = client.get(
            "/api/authors/",
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        assert response.status_code == 200
        assert response.json() == []
    
    def test_create_author_success(self, client: TestClient, test_user_token: str):
        """Test: POST /api/authors/ crear autor exitosamente"""
        author_data = {
            "name": "Gabriel García Márquez",
            "nationality": "Colombiana",
            "date_of_birth": "1927-03-06"
        }
        response = client.post(
            "/api/authors/",
            json=author_data,
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Gabriel García Márquez"
        assert data["nationality"] == "Colombiana"
        assert "id" in data
    
    def test_create_author_without_auth(self, client: TestClient):
        """Test: POST /api/authors/ sin autenticación debe fallar"""
        author_data = {"name": "Test Author"}
        response = client.post("/api/authors/", json=author_data)
        assert response.status_code == 401
    
    def test_get_author_by_id_success(self, client: TestClient, test_user_token: str, db_session):
        """Test: GET /api/authors/{id} obtener autor exitosamente"""
        # Crear autor
        author = Author(name="Test Author", nationality="Test")
        db_session.add(author)
        db_session.commit()
        db_session.refresh(author)
        
        response = client.get(
            f"/api/authors/{author.id}",
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == author.id
        assert data["name"] == "Test Author"
    
    def test_get_author_by_id_not_found(self, client: TestClient, test_user_token: str):
        """Test: GET /api/authors/{id} con ID inexistente"""
        response = client.get(
            "/api/authors/999",
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
    
    def test_update_author_success(self, client: TestClient, test_user_token: str, db_session):
        """Test: PUT /api/authors/{id} actualizar autor exitosamente"""
        author = Author(name="Original Name", nationality="Original")
        db_session.add(author)
        db_session.commit()
        db_session.refresh(author)
        
        update_data = {
            "name": "Updated Name",
            "nationality": "Updated"
        }
        response = client.put(
            f"/api/authors/{author.id}",
            json=update_data,
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Name"
        assert data["nationality"] == "Updated"
    
    def test_delete_author_success(self, client: TestClient, test_user_token: str, db_session):
        """Test: DELETE /api/authors/{id} eliminar autor exitosamente"""
        author = Author(name="To Delete", nationality="Test")
        db_session.add(author)
        db_session.commit()
        db_session.refresh(author)
        
        response = client.delete(
            f"/api/authors/{author.id}",
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        assert response.status_code == 200
        assert "deleted successfully" in response.json()["message"]


class TestBookEndpoints:
    """Tests para los endpoints de libros"""
    
    @pytest.fixture
    def test_author(self, db_session):
        """Fixture: Crea un autor de prueba"""
        author = Author(name="Test Author", nationality="Test")
        db_session.add(author)
        db_session.commit()
        db_session.refresh(author)
        return author
    
    def test_get_books_empty(self, client: TestClient, test_user_token: str):
        """Test: GET /api/books/ con lista vacía"""
        response = client.get(
            "/api/books/",
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        assert response.status_code == 200
        assert response.json() == []
    
    def test_create_book_success(self, client: TestClient, test_user_token: str, test_author: Author):
        """Test: POST /api/books/ crear libro exitosamente"""
        book_data = {
            "title": "Cien años de soledad",
            "isbn": "978-84-376-0494-7",
            "author_id": test_author.id,
            "published_year": 1967,
            "genre": "Realismo mágico",
            "isAvailable": True
        }
        response = client.post(
            "/api/books/",
            json=book_data,
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Cien años de soledad"
        assert data["isbn"] == "978-84-376-0494-7"
        assert data["author"]["id"] == test_author.id
    
    def test_create_book_without_auth(self, client: TestClient, test_author: Author):
        """Test: POST /api/books/ sin autenticación debe fallar"""
        book_data = {
            "title": "Test Book",
            "isbn": "1234567890",
            "author_id": test_author.id
        }
        response = client.post("/api/books/", json=book_data)
        assert response.status_code == 401
    
    def test_create_book_author_not_found(self, client: TestClient, test_user_token: str):
        """Test: POST /api/books/ con autor inexistente"""
        book_data = {
            "title": "Test Book",
            "isbn": "1234567890",
            "author_id": 999
        }
        response = client.post(
            "/api/books/",
            json=book_data,
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        assert response.status_code == 404
        assert "author" in response.json()["detail"].lower()
    
    def test_get_book_by_id_success(self, client: TestClient, test_user_token: str, test_author: Author, db_session):
        """Test: GET /api/books/{id} obtener libro exitosamente"""
        book = Book(
            title="Test Book",
            isbn="1234567890",
            author_id=test_author.id
        )
        db_session.add(book)
        db_session.commit()
        db_session.refresh(book)
        
        response = client.get(
            f"/api/books/{book.id}",
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == book.id
        assert data["title"] == "Test Book"
        assert "author" in data
    
    def test_get_books_with_filters(self, client: TestClient, test_user_token: str, test_author: Author, db_session):
        """Test: GET /api/books/ con filtros"""
        # Crear libros
        book1 = Book(title="Available Book", isbn="111", author_id=test_author.id, is_available=True)
        book2 = Book(title="Unavailable Book", isbn="222", author_id=test_author.id, is_available=False)
        db_session.add(book1)
        db_session.add(book2)
        db_session.commit()
        
        # Filtrar por disponibilidad
        response = client.get(
            "/api/books/?isAvailable=true",
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        assert response.status_code == 200
        books = response.json()
        assert len(books) == 1
        assert books[0]["title"] == "Available Book"
        
        # Filtrar por título
        response = client.get(
            "/api/books/?title=Available",
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        assert response.status_code == 200
        books = response.json()
        assert len(books) == 1
    
    def test_update_book_success(self, client: TestClient, test_user_token: str, test_author: Author, db_session):
        """Test: PUT /api/books/{id} actualizar libro exitosamente"""
        book = Book(title="Original Title", isbn="123", author_id=test_author.id)
        db_session.add(book)
        db_session.commit()
        db_session.refresh(book)
        
        update_data = {
            "title": "Updated Title",
            "genre": "New Genre"
        }
        response = client.put(
            f"/api/books/{book.id}",
            json=update_data,
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["genre"] == "New Genre"
    
    def test_delete_book_success(self, client: TestClient, test_user_token: str, test_author: Author, db_session):
        """Test: DELETE /api/books/{id} eliminar libro exitosamente"""
        book = Book(title="To Delete", isbn="123", author_id=test_author.id)
        db_session.add(book)
        db_session.commit()
        db_session.refresh(book)
        
        response = client.delete(
            f"/api/books/{book.id}",
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        assert response.status_code == 200
        assert "deleted successfully" in response.json()["message"]


class TestUserEndpoints:
    """Tests para los endpoints de usuarios y autenticación"""
    
    def test_register_user_success(self, client: TestClient):
        """Test: POST /api/users/register registrar usuario exitosamente"""
        user_data = {
            "username": "newuser",
            "password": "password123"
        }
        response = client.post("/api/users/register", json=user_data)
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "newuser"
        assert "password" not in data  # Password no debe estar en la respuesta
    
    def test_register_user_duplicate(self, client: TestClient):
        """Test: POST /api/users/register con username duplicado debe fallar"""
        user_data = {
            "username": "duplicateuser",
            "password": "password123"
        }
        # Primer registro
        client.post("/api/users/register", json=user_data)
        # Segundo registro (debe fallar)
        response = client.post("/api/users/register", json=user_data)
        assert response.status_code == 400
        assert "already taken" in response.json()["detail"].lower()
    
    def test_login_success(self, client: TestClient):
        """Test: POST /api/users/login login exitoso"""
        user_data = {
            "username": "loginuser",
            "password": "password123"
        }
        # Registrar usuario
        client.post("/api/users/register", json=user_data)
        # Hacer login
        response = client.post("/api/users/login", json=user_data)
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert len(data["access_token"]) > 0
    
    def test_login_invalid_credentials(self, client: TestClient):
        """Test: POST /api/users/login con credenciales inválidas"""
        user_data = {
            "username": "nonexistent",
            "password": "wrongpassword"
        }
        response = client.post("/api/users/login", json=user_data)
        assert response.status_code == 401
        assert "invalid" in response.json()["detail"].lower()
    
    def test_get_profile_success(self, client: TestClient, test_user_token: str):
        """Test: GET /api/users/profile obtener perfil exitosamente"""
        response = client.get(
            "/api/users/profile",
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        assert response.status_code == 200
        assert "Welcome" in response.json()["message"]
    
    def test_get_profile_without_auth(self, client: TestClient):
        """Test: GET /api/users/profile sin autenticación debe fallar"""
        response = client.get("/api/users/profile")
        assert response.status_code == 401

