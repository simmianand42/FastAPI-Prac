from fastapi import FastAPI, Body, HTTPException, Path, Query
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
    id: Optional[int] = Field(title='id id not needed') # Optional variables need a =None example -> id: Optional[int] = None
    title: str = Field(min_length = 6)
    author: str = Field(min_legth = 6)
    description: str = Field(min_length=10, max_length= 100)
    category: str = Field(min_length = 5)

    class Config:
        schema_extra = {  # use json_schema_extra if using Pydantics v2
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

@app.get("/books/{book_id}")
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail='Item not found')

@app.get("/books/")
async def read_book_by_query(book_id: int = Query(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail='Item not found')


# Without validation
@app.post("/books/create_book")
async def create_book(book_request = Body()):
    BOOKS.append(book_request)

# With Validation
@app.post("/books/valid_create_book")
async def create_valid_book(book_request: BookRequest):
    new_book = Book(**book_request.dict())  # use .model_dump() instead of .dict() function for Pydantics v2
    BOOKS.append(find_book_id(new_book))
    
def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book


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

@app.delete("/books/{book_id}")
async def delete_book(book_id: int = Path(gt=0)):
    book_deleted = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_deleted = True
            break
    if not book_deleted:
        raise HTTPException(status_code=404, detail = 'Item not found')
    


