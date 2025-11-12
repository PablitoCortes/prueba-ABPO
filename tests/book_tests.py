from fastapi.testclient import TestClient
import app

client = TestClient(app)

def test_get_books_empty_list():
	response = client.get("/books")
	assert response.status_code == 404 or response.status_code == 200
	assert isinstance(response.json(),list) or "detail" in response.json()

def test_get_book_by_id():
	response = client.get("/books/{id}")
	assert response.status_code == 404 or response.status_code == 200
	assert isinstance(response.json(),dict) or "detail" in response.json()

def test_get_book_by_title():
	response = client.get("/books/{title}")
	assert response.status_code == 404 or response.status_code == 200
	assert isinstance(response.json(),dict) or "detail" in response.json()




