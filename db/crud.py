from fastapi import HTTPException
from sqlalchemy.orm import Session, aliased
from sqlalchemy import func, and_

from . import schemas, decorators
from .models import Book, ShopBooks, Shop, BookPrice

@decorators.check_slug_book
def get_book(db: Session, book_slug: str):
    q = db.query(Book).filter(Book.slug == book_slug)
    return q.first()


def get_books(db: Session):
    return db.query(Book).all()


def create_book(db: Session, book: schemas.BookIn):
    q_book = db.query(Book).filter(Book.slug == book.slug)

    if db.query(q_book.exists()):
        raise HTTPException(status_code=400, detail='book already created')

    if book.shop is not None and not _is_shop(db, book.shop.shop_id):
        raise HTTPException(status_code=404, detail=f'shop id:{book.shop.shop_id} not found')

    db_shop = Shop(**book.shop.dict())
    db_book = Book(**book.dict())

    db.add(db_shop, db_book)
    db.commit()
    return db_book


@decorators.check_slug_book
def get_book_prices(db: Session, book_slug, last_prices):
    if last_prices:
        q = db.query(
            BookPrice.book_slug,
            BookPrice.shop_id,
            func.max(BookPrice.date).label('date')
        ).group_by(
            BookPrice.shop_id,
            BookPrice.book_slug
        ).subquery()

        q = db.query(BookPrice).select_from(q).join(
            BookPrice, and_(
                BookPrice.shop_id == q.c.shop_id,
                BookPrice.book_slug == q.c.book_slug,
                BookPrice.date == q.c.date
            )
        ).filter(BookPrice.book_slug == book_slug)
        return q.all()
    return _get_all_prices(db, book_slug).all()


# db.query(models.BookPrice).filter(models.BookPrice.book_slug == book_slug).all()


@decorators.check_slug_book
def create_book_prices(db: Session, book_slug: str, price: schemas.Prices):
    if not _is_shop(db, price.shop_id):
        raise HTTPException(status_code=404, detail=f'shop id:{price.shop_id} not found')

    db_price = BookPrice(**price.dict())
    db.add(db_price)
    db.commit()

    return price


def _is_shop(db: Session, shop_id: int):
    q = db.query(Shop).filter(Shop.id == shop_id)
    return db.query(q.exists())


def _get_all_prices(db: Session, book_slug):
    return db.query(BookPrice).filter(BookPrice.book_slug == book_slug)
