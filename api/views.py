from typing import List
from fastapi import Depends, status

from db.schemas import (
    BookIn,
    BookOut,
    PriceIn,
    PriceOut,
    ShopIn,
    ShopOut,
    ShopBookIn,
    ShopBookOut,
    ParserBookIn,
    ParserBookOut
)
from db.connector import Session
from db import crud

from .tasks import create_or_upd_book
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
    response_model=List[PriceOut]
)
def get_book_prices(book_slug: str, db: Session = Depends(get_db),
                    last_prices: bool = False):
    return crud.get_book_prices(db, last_prices, book_slug=book_slug)


@app.post(
    '/books/{book_slug}/prices',
    status_code=201,
    response_model=PriceOut
)
def create_book_price(book_slug: str, price: PriceIn,
                      db: Session = Depends(get_db)):
    return crud.create_book_prices(db, price, book_slug=book_slug, shop_id=price.shop_id)


@app.post(
    '/books/{book_slug}/urls',
    status_code=201,
    response_model=ShopBookOut
)
def create_shop_book(book_slug: str, shop_book: ShopBookIn,
                     db: Session = Depends(get_db)):
    return crud.create_shop_book(db, shop_book, book_slug=book_slug, shop_id=shop_book.shop_id)


@app.get(
    '/books/{book_slug}/urls',
    status_code=200,
    response_model=List[ShopBookOut]
)
def get_shop_books(book_slug: str, db: Session = Depends(get_db)):
    return crud.get_shop_books(db, book_slug=book_slug)


@app.get(
    '/books/{book_slug}',
    status_code=status.HTTP_200_OK,
    response_model=BookOut
)
def get_book(book_slug: str, db: Session = Depends(get_db)):
    return crud.get_book(db, book_slug=book_slug)


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
def create_book(book: BookIn, db: Session = Depends(get_db)):
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


@app.post(
    '/systems/parser',
    status_code=status.HTTP_200_OK,
)
def create_book_parser(book: ParserBookIn):
    create_or_upd_book.delay(book.dict())
# TODO PUT REQUESTS Shops, Book, Prices
