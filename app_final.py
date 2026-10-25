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
