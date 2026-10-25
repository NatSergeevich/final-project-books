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

def test_add_book_with_missing_fields():
    """Тест 4: Проверка валидации - сервер должен отклонить запрос без обязательных полей"""
    payload = {"title": "1984"}  # Нет author и year
    response = client.post("/books", json=payload)
    assert response.status_code == 422  # 422 = Unprocessable Entity (ошибка валидации)

def test_book_response_structure():
    """Тест 5: Проверка структуры ответа - все нужные поля должны быть на месте"""
    payload = {"title": "Test Book", "author": "Test Author", "year": 2024}
    response = client.post("/books", json=payload)
    data = response.json()
    
    # Проверяем, что в ответе есть все нужные поля
    assert "id" in data
    assert "title" in data
    assert "author" in data
    assert "year" in data
    assert "added_at" in data
