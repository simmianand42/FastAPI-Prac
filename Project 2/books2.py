from fastapi import FastAPI, Body, HTTPException
from pydantic import BaseModel, Field

from typing import Optional

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    category: str

    def __init__(self, id, title, author, description, category):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.category = category

class BookRequest(BaseModel):
    id: Optional[int] = Field(title='id id not needed')
    title: str = Field(min_length = 6)
    author: str = Field(min_legth = 6)
    description: str = Field(min_length=10, max_length= 100)
    category: str = Field(min_length = 5)

    class Config:
        schema_extra = {
            'example': {
                'title' : 'A new book',
                'author' : 'Coding with Me',
                'description': 'A new description',
                'category': 'sample'
            }
        }

BOOKS = [
    Book(1,'Title One', 'Author One', 'A very nice book', 'science'),
    Book(2, 'Title Two', 'Author Two', 'A very nice book',  'science'),
    Book(3, 'Title Three', 'Author Three', 'A very nice book','history'),
    Book(4, 'Title Four', 'Author Four', 'A very nice book','history'),
    Book(5,'Title Five', 'Author One', 'A very nice book', 'maths')
]


@app.get("/books")
async def get_all():
    return BOOKS

@app.post("/books/create_book")
async def create_book(book_request = Body()):
    BOOKS.append(book_request)

# Without Validation
@app.put("/books/invalid_id_update/{book_title}")
async def update_book_invalid(book_title: str, book = Body()):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].title == book_title.casefold():
            BOOKS[i] = book

# With validation
@app.put("/books/update_book/{book_id}")
async def update_book(book_id: int, book: BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS[i].title = book.title
            BOOKS[i].description = book.description
            BOOKS[i].category = book.category
            BOOKS[i].author = book.author
            book_changed = True
    if not book_changed:
        raise HTTPException(status_code=404, detail='Item not found')
