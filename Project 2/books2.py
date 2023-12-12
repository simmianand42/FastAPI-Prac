from fastapi import FastAPI

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    decription: str
    category: str

    def __init__(self, id, title, author, decrption, category):
        self.id = id
        self.title = title
        self.author = author
        self.decription = decrption
        self.category = category


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
