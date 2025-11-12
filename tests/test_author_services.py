import pytest
from sqlalchemy.orm import Session
from services.authors import author_services
from services.exceptions import NotFoundError, BadRequestError
from schemas.author_schema import CreateAuthorSchema, UpdateAuthorSchema
from models.author_model import Author
from tests.conftest import db_session


class TestAuthorServices:
    """Tests unitarios para los servicios de autores"""
    
    def test_create_author_success(self, db_session: Session):
        """Test: Crear autor exitosamente"""
        author_data = CreateAuthorSchema(
            name="Gabriel García Márquez",
            nationality="Colombiana",
            date_of_birth="1927-03-06"
        )
        
        author = author_services.create_author(db_session, author_data)
        
        assert author.id is not None
        assert author.name == "Gabriel García Márquez"
        assert author.nationality == "Colombiana"
        assert author.date_of_birth == "1927-03-06"
    
    def test_create_author_missing_name(self, db_session: Session):
        """Test: Crear autor sin nombre debe fallar"""
        author_data = CreateAuthorSchema(
            name="",
            nationality="Colombiana"
        )
        
        with pytest.raises(BadRequestError, match="Name is required"):
            author_services.create_author(db_session, author_data)
    
    def test_get_authors_empty(self, db_session: Session):
        """Test: Obtener lista de autores vacía"""
        authors = author_services.get_authors(db_session)
        assert authors == []
    
    def test_get_authors_with_data(self, db_session: Session):
        """Test: Obtener lista de autores con datos"""
        # Crear autores de prueba
        author1 = Author(name="Autor 1", nationality="Nacionalidad 1")
        author2 = Author(name="Autor 2", nationality="Nacionalidad 2")
        db_session.add(author1)
        db_session.add(author2)
        db_session.commit()
        
        authors = author_services.get_authors(db_session)
        
        assert len(authors) == 2
        assert authors[0].name == "Autor 1"
        assert authors[1].name == "Autor 2"
    
    def test_get_author_by_id_success(self, db_session: Session):
        """Test: Obtener autor por ID exitosamente"""
        author = Author(name="Test Author", nationality="Test Nationality")
        db_session.add(author)
        db_session.commit()
        db_session.refresh(author)
        
        found_author = author_services.get_author_by_id(db_session, author.id)
        
        assert found_author is not None
        assert found_author.id == author.id
        assert found_author.name == "Test Author"
    
    def test_get_author_by_id_not_found(self, db_session: Session):
        """Test: Obtener autor por ID inexistente"""
        found_author = author_services.get_author_by_id(db_session, 999)
        assert found_author is None
    
    def test_update_author_success(self, db_session: Session):
        """Test: Actualizar autor exitosamente"""
        author = Author(name="Original Name", nationality="Original Nationality")
        db_session.add(author)
        db_session.commit()
        db_session.refresh(author)
        
        update_data = UpdateAuthorSchema(
            name="Updated Name",
            nationality="Updated Nationality"
        )
        
        updated_author = author_services.update_author(db_session, author.id, update_data)
        
        assert updated_author.name == "Updated Name"
        assert updated_author.nationality == "Updated Nationality"
    
    def test_update_author_not_found(self, db_session: Session):
        """Test: Actualizar autor inexistente debe fallar"""
        update_data = UpdateAuthorSchema(name="New Name")
        
        with pytest.raises(NotFoundError, match="Author not found"):
            author_services.update_author(db_session, 999, update_data)
    
    def test_update_author_partial(self, db_session: Session):
        """Test: Actualizar solo algunos campos del autor"""
        author = Author(name="Original Name", nationality="Original Nationality")
        db_session.add(author)
        db_session.commit()
        db_session.refresh(author)
        
        update_data = UpdateAuthorSchema(nationality="New Nationality")
        
        updated_author = author_services.update_author(db_session, author.id, update_data)
        
        assert updated_author.name == "Original Name"  # No cambió
        assert updated_author.nationality == "New Nationality"  # Cambió
    
    def test_delete_author_success(self, db_session: Session):
        """Test: Eliminar autor exitosamente"""
        author = Author(name="To Delete", nationality="Test")
        db_session.add(author)
        db_session.commit()
        db_session.refresh(author)
        author_id = author.id
        
        deleted_author = author_services.delete_author(db_session, author_id)
        
        assert deleted_author.id == author_id
        # Verificar que fue eliminado
        found = db_session.query(Author).filter(Author.id == author_id).first()
        assert found is None
    
    def test_delete_author_not_found(self, db_session: Session):
        """Test: Eliminar autor inexistente debe fallar"""
        with pytest.raises(NotFoundError, match="Author not found"):
            author_services.delete_author(db_session, 999)
    
    def test_delete_author_with_books(self, db_session: Session):
        """Test: Eliminar autor con libros asociados debe fallar"""
        from models.book_model import Book
        
        author = Author(name="Author with Books", nationality="Test")
        db_session.add(author)
        db_session.commit()
        db_session.refresh(author)
        
        book = Book(
            title="Test Book",
            isbn="1234567890",
            author_id=author.id
        )
        db_session.add(book)
        db_session.commit()
        
        with pytest.raises(BadRequestError, match="Cannot delete this author"):
            author_services.delete_author(db_session, author.id)

