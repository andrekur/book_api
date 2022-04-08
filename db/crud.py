from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, and_

from . import schemas, decorators
from .models import BookModel, ShopModel, BookPriceModel, ShopBooksModel


@decorators.check_slug_book
def get_book(db: Session, book_slug: str):
    q = db.query(BookModel).filter(BookModel.slug == book_slug)
    return q.first()


def get_books(db: Session):
    return db.query(BookModel).all()


def create_book(db: Session, book: schemas.BookIn):
    q = db.query(BookModel).filter(BookModel.slug == book.slug).exists()
    if db.query(q).scalar():
        raise HTTPException(status_code=404, detail='book already created')

    db_book = BookModel(**book.dict())
    db.add(db_book)
    db.commit()
    return db_book


@decorators.check_slug_book
def get_book_prices(db: Session, book_slug, last_prices):
    if last_prices:
        q = db.query(
            BookPriceModel.book_slug,
            BookPriceModel.shop_id,
            func.max(BookPriceModel.date).label('date')
        ).group_by(
            BookPriceModel.shop_id,
            BookPriceModel.book_slug
        ).subquery()

        q = db.query(BookPriceModel).select_from(q).join(
            BookPriceModel, and_(
                BookPriceModel.shop_id == q.c.shop_id,
                BookPriceModel.book_slug == q.c.book_slug,
                BookPriceModel.date == q.c.date
            )
        ).filter(BookPriceModel.book_slug == book_slug)
        return q.all()
    return _get_all_prices(db, book_slug).all()


@decorators.check_slug_book
def create_book_prices(db: Session, book_slug: str, price: schemas.PriceIn):
    if not _is_shop_by_id(db, price.shop_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'shop id:{price.shop_id} not found')

    db_price = BookPriceModel(**price.dict())
    db.add(db_price)
    db.commit()

    return db_price


def create_shop(db: Session, shop: schemas.ShopIn):
    if _is_shop_by_name(db, shop.name):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'shop already created')
    db_shop = ShopModel(**shop.dict())
    db.add(db_shop)
    db.commit()
    return db_shop


def get_shops(db: Session):
    return db.query(ShopModel).all()


def _is_shop_by_id(db: Session, shop_id: int):
    q = db.query(ShopModel).filter(ShopModel.id == shop_id).exists()
    return db.query(q).scalar()


def _is_shop_by_name(db: Session, shop_name: str):
    q = db.query(ShopModel).filter(ShopModel.name == shop_name).exists()
    return db.query(q).scalar()


def _get_all_prices(db: Session, book_slug):
    return db.query(BookPriceModel).filter(BookPriceModel.book_slug == book_slug)
