import os
import logging
import uuid
from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

APP_NAME = os.getenv("APP_NAME", "BookCatalog")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

logging.basicConfig(level=LOG_LEVEL, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(APP_NAME)

app = FastAPI(title=APP_NAME, version=APP_VERSION)

books_db = []

class BookCreate(BaseModel):
    title: str
    author: str
    year: int

class Book(BookCreate):
    id: str
    added_at: str

@app.on_event("startup")
async def startup_event():
    logger.info(f"Приложение {APP_NAME} версии {APP_VERSION} успешно запущено.")

@app.get("/health")
def health_check():
    return {"status": "ok", "service": APP_NAME}

@app.get("/version")
def get_version():
    return {"version": APP_VERSION}

# --- Бизнес-маршруты ---

@app.post("/books", status_code=201)
def add_book(book: BookCreate):
    new_id = str(uuid.uuid4())
    new_book = Book(
        id=new_id,
        added_at=datetime.now().isoformat(),
        **book.model_dump()
    )
    books_db.append(new_book)
    logger.info(f"Добавлена новая книга: '{new_book.title}' автор {new_book.author}")
    return new_book

@app.get("/books")
def get_all_books():
    logger.info(f"Запрошен список всех книг. Всего в каталоге: {len(books_db)}")
    return {"books": books_db}

@app.get("/books/{book_id}")
def get_book_by_id(book_id: str):
    for book in books_db:
        if book.id == book_id:
            return book
    logger.warning(f"Книга с ID {book_id} не найдена.")
    raise HTTPException(status_code=404, detail="Книга не найдена")
