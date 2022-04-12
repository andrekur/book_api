from .models import BookModel, ShopModel
from fastapi import HTTPException


def check_slug_book(func):
    def wrapper(db, book_slug: str, *args, **kwargs):
        q = db.query(BookModel).filter(BookModel.slug == book_slug).exists()
        if not db.query(q).scalar():
            raise HTTPException(status_code=404, detail='book not found')
        return func(db, book_slug, *args, **kwargs)
    return wrapper
