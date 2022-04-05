from .models import Book

from fastapi import HTTPException


def check_slug_book(func):
    def wrapper(*args, **kwargs):
        db, book_slug, _ = args

        q = db.query(Book).filter(Book.slug == book_slug)
        if not db.query(q.exists()):
            raise HTTPException(status_code=404, detail='book not found')
        return func(*args, **kwargs)
    return wrapper
