from .api_start import app
from .models import Book
from .tasks import add_book as add


@app.post('/book')
def add_book(book: Book):
    add.delay(book.name)
    return f'1'
