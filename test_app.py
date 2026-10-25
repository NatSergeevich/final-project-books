from fastapi.testclient import TestClient
from app_final import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_add_book_endpoint():
    payload = {"title": "1984", "author": "George Orwell", "year": 1949}
    response = client.post("/books", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "1984"
    assert "id" in data

def test_get_book_by_id_and_not_found():
    # Сначала добавляем книгу, чтобы получить её ID
    payload = {"title": "Dune", "author": "Frank Herbert", "year": 1965}
    post_response = client.post("/books", json=payload)
    book_id = post_response.json()["id"]
    
    # Проверяем успешное получение по параметру (ID)
    get_response = client.get(f"/books/{book_id}")
    assert get_response.status_code == 200
    assert get_response.json()["author"] == "Frank Herbert"
    
    # Проверяем обработку ошибки (книга не найдена)
    error_response = client.get("/books/non-existent-id")
    assert error_response.status_code == 404
