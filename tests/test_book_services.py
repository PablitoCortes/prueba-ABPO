import pytest
from sqlalchemy.orm import Session
from services.books import book_services
from services.exceptions import NotFoundError, BadRequestError
from schemas.book_schema import CreateBookSchema, UpdateBookSchema
from models.book_model import Book
from models.author_model import Author
from tests.conftest import db_session


class TestBookServices:
    """Tests unitarios para los servicios de libros"""
    
    @pytest.fixture
    def test_author(self, db_session: Session):
        """Fixture: Crea un autor de prueba"""
        author = Author(name="Test Author", nationality="Test")
        db_session.add(author)
        db_session.commit()
        db_session.refresh(author)
        return author
    
    def test_create_book_success(self, db_session: Session, test_author: Author):
        """Test: Crear libro exitosamente"""
        book_data = CreateBookSchema(
            title="Cien años de soledad",
            isbn="978-84-376-0494-7",
            author_id=test_author.id,
            published_year=1967,
            genre="Realismo mágico",
            isAvailable=True
        )
        
        book = book_services.create_book(db_session, book_data)
        
        assert book.id is not None
        assert book.title == "Cien años de soledad"
        assert book.isbn == "978-84-376-0494-7"
        assert book.author_id == test_author.id
        assert book.published_year == 1967
    
    def test_create_book_missing_data(self, db_session: Session, test_author: Author):
        """Test: Crear libro sin datos requeridos debe fallar"""
        book_data = CreateBookSchema(
            title="",  # Título vacío
            isbn="978-84-376-0494-7",
            author_id=test_author.id
        )
        
        with pytest.raises(BadRequestError, match="Missing data"):
            book_services.create_book(db_session, book_data)
    
    def test_create_book_author_not_found(self, db_session: Session):
        """Test: Crear libro con autor inexistente debe fallar"""
        book_data = CreateBookSchema(
            title="Test Book",
            isbn="978-84-376-0494-7",
            author_id=999  # ID inexistente
        )
        
        with pytest.raises(NotFoundError, match="Author not found"):
            book_services.create_book(db_session, book_data)
    
    def test_create_book_duplicate_isbn(self, db_session: Session, test_author: Author):
        """Test: Crear libro con ISBN duplicado debe fallar"""
        isbn = "978-84-376-0494-7"
        
        # Crear primer libro
        book_data1 = CreateBookSchema(
            title="Book 1",
            isbn=isbn,
            author_id=test_author.id
        )
        book_services.create_book(db_session, book_data1)
        
        # Intentar crear segundo libro con mismo ISBN
        book_data2 = CreateBookSchema(
            title="Book 2",
            isbn=isbn,
            author_id=test_author.id
        )
        
        with pytest.raises(BadRequestError, match="ISBN already exists"):
            book_services.create_book(db_session, book_data2)
    
    def test_get_books_empty(self, db_session: Session):
        """Test: Obtener lista de libros vacía"""
        books = book_services.get_books(db_session)
        assert books == []
    
    def test_get_books_with_pagination(self, db_session: Session, test_author: Author):
        """Test: Obtener libros con paginación"""
        # Crear 15 libros
        for i in range(15):
            book = Book(
                title=f"Book {i}",
                isbn=f"123456789{i:02d}",
                author_id=test_author.id
            )
            db_session.add(book)
        db_session.commit()
        
        # Primera página (10 libros)
        books_page1 = book_services.get_books(db_session, page=1, limit=10)
        assert len(books_page1) == 10
        
        # Segunda página (5 libros)
        books_page2 = book_services.get_books(db_session, page=2, limit=10)
        assert len(books_page2) == 5
    
    def test_get_books_filter_by_availability(self, db_session: Session, test_author: Author):
        """Test: Filtrar libros por disponibilidad"""
        # Crear libros disponibles y no disponibles
        book1 = Book(title="Available Book", isbn="111", author_id=test_author.id, is_available=True)
        book2 = Book(title="Unavailable Book", isbn="222", author_id=test_author.id, is_available=False)
        db_session.add(book1)
        db_session.add(book2)
        db_session.commit()
        
        available_books = book_services.get_books(db_session, isAvailable=True)
        
        assert len(available_books) == 1
        assert available_books[0].title == "Available Book"
    
    def test_get_books_filter_by_title(self, db_session: Session, test_author: Author):
        """Test: Filtrar libros por título"""
        book1 = Book(title="Cien años de soledad", isbn="111", author_id=test_author.id)
        book2 = Book(title="El amor en los tiempos del cólera", isbn="222", author_id=test_author.id)
        db_session.add(book1)
        db_session.add(book2)
        db_session.commit()
        
        filtered_books = book_services.get_books(db_session, title="Cien")
        
        assert len(filtered_books) == 1
        assert filtered_books[0].title == "Cien años de soledad"
    
    def test_get_book_by_id_success(self, db_session: Session, test_author: Author):
        """Test: Obtener libro por ID exitosamente"""
        book = Book(title="Test Book", isbn="123", author_id=test_author.id)
        db_session.add(book)
        db_session.commit()
        db_session.refresh(book)
        
        found_book = book_services.get_book_by_id(db_session, book.id)
        
        assert found_book is not None
        assert found_book.id == book.id
        assert found_book.title == "Test Book"
        assert found_book.author is not None  # Verificar que carga la relación
    
    def test_get_book_by_id_not_found(self, db_session: Session):
        """Test: Obtener libro por ID inexistente"""
        found_book = book_services.get_book_by_id(db_session, 999)
        assert found_book is None
    
    def test_update_book_success(self, db_session: Session, test_author: Author):
        """Test: Actualizar libro exitosamente"""
        book = Book(title="Original Title", isbn="123", author_id=test_author.id)
        db_session.add(book)
        db_session.commit()
        db_session.refresh(book)
        
        update_data = UpdateBookSchema(
            title="Updated Title",
            genre="New Genre"
        )
        
        updated_book = book_services.update_book(db_session, book.id, update_data)
        
        assert updated_book.title == "Updated Title"
        assert updated_book.genre == "New Genre"
    
    def test_update_book_not_found(self, db_session: Session):
        """Test: Actualizar libro inexistente debe fallar"""
        update_data = UpdateBookSchema(title="New Title")
        
        with pytest.raises(NotFoundError, match="Book not found"):
            book_services.update_book(db_session, 999, update_data)
    
    def test_update_book_author_not_found(self, db_session: Session, test_author: Author):
        """Test: Actualizar libro con autor inexistente debe fallar"""
        book = Book(title="Test Book", isbn="123", author_id=test_author.id)
        db_session.add(book)
        db_session.commit()
        db_session.refresh(book)
        
        update_data = UpdateBookSchema(author_id=999)
        
        with pytest.raises(NotFoundError, match="Author not found"):
            book_services.update_book(db_session, book.id, update_data)
    
    def test_delete_book_success(self, db_session: Session, test_author: Author):
        """Test: Eliminar libro exitosamente"""
        book = Book(title="To Delete", isbn="123", author_id=test_author.id)
        db_session.add(book)
        db_session.commit()
        db_session.refresh(book)
        book_id = book.id
        
        deleted_book = book_services.delete_book(db_session, book_id)
        
        assert deleted_book.id == book_id
        # Verificar que fue eliminado
        found = db_session.query(Book).filter(Book.id == book_id).first()
        assert found is None
    
    def test_delete_book_not_found(self, db_session: Session):
        """Test: Eliminar libro inexistente debe fallar"""
        with pytest.raises(NotFoundError, match="Book not found"):
            book_services.delete_book(db_session, 999)

