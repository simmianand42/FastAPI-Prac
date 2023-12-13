from fastapi import FastAPI, Body

app = FastAPI()

BOOKS = [
{'title': 'Title One', 'author': 'Author One', 'category': 'science'}, 
{'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
{'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
{'title': 'Title Four', 'author': 'Author Four', 'category': 'history'},
{'title': 'Title Five', 'author': 'Author One', 'category': 'maths'}
]

@app.get("/books")
async def get_all():
    return BOOKS

@app.get("/books/{book_title}")
async def read_book(book_title: str):
    for book in BOOKS:
        if book['title'].casefold() == book_title.casefold():
            return book

@app.get("/books/")
async def read_category_by_query(category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return

# Get all books from a specific author using path or query parameter
@app.get("/books/byauthor/{book_author}")
async def read_books_by_author_path(book_author: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == book_author.casefold():
            books_to_return.append(book)

    return books_to_return

@app.get("/books/byauthor/{book_author}/")
async def read_author_category(book_author: str, category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == book_author.casefold() and \
                book.get('category').casefold() == category.casefold():
            books_to_return.append(book)

    return books_to_return

@app.post("/books/create_book")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)

@app.put("/books/update_book")
async def update_book(updated_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == updated_book.get('title').casefold():
            BOOKS[i] = updated_book

@app.put("/books/update_book_param/{book_title}")
async def update_book_param(book_title:str, updated_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            BOOKS[i] = updated_book
            
@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            BOOKS.pop(i)
            break

@app.put("/books/update_new/{book_title}")
async def new_update(book_title:str, updated_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            BOOKS[i]['category'] = updated_book.get('category')
