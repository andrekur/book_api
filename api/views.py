from typing import List
from fastapi import Depends, status

from db.schemas import BookIn, BookOut, Price, ShopIn, ShopOut
from db.connector import Session
from db import crud

from . import tasks
from .api_start import app


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


@app.get(
    '/books/{book_slug}/prices',
    status_code=status.HTTP_200_OK,
    response_model=List[Price]
)
def get_book_prices(book_slug: str, db: Session = Depends(get_db), last_prices: bool = False):
    return crud.get_book_prices(db, book_slug, last_prices)


@app.post(
    '/books/{book_slug}/prices',
    status_code=201,
    response_model=Price
)
def create_book_price(book_slug: str, price: Price, db: Session = Depends(get_db)):
    return crud.create_book_prices(db, book_slug, price)


@app.get(
    '/books/{book_slug}',
    status_code=status.HTTP_200_OK,
    response_model=BookOut
)
def get_book(book_slug: str, db: Session = Depends(get_db)):
    return crud.get_book(db, book_slug)


@app.get(
    '/books',
    status_code=status.HTTP_200_OK,
    response_model=List[BookOut]
)
def get_books(db: Session = Depends(get_db)):
    return crud.get_books(db)


@app.post(
    '/books',
    status_code=status.HTTP_201_CREATED,
    response_model=BookOut
)
def create_book(book: BookIn, db: Session = Depends(get_db), parser: bool = False):
    if parser:
        tasks.create_book.delay(book.name)
        return book
    return crud.create_book(db, book)


@app.post(
    '/shops',
    status_code=status.HTTP_201_CREATED,
    response_model=ShopOut
)
def create_shop(shop: ShopIn, db: Session = Depends(get_db)):
    return crud.create_shop(db, shop)


@app.get(
    '/shops',
    status_code=status.HTTP_200_OK,
    response_model=List[ShopOut]
)
def get_shops(db: Session = Depends(get_db)):
    return crud.get_shops(db)

# TODO PUT REQUESTS Shops, Book
