from .models import BookModel

from fastapi import HTTPException


def check_slug_book(func):
    def wrapper(*args, **kwargs):
        db, book_slug = args[0:2]

        q = db.query(BookModel).filter(BookModel.slug == book_slug)
        if not db.query(q.exists()):
            raise HTTPException(status_code=404, detail='book not found')
        return func(*args, **kwargs)
    return wrapper
