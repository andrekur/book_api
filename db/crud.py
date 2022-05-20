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
    return _get_all_prices(db, book_slug)


@decorators.check_slug_book
def create_book_prices(db: Session, book_slug: str,
                       price: schemas.PriceIn):
    if not _is_shop_by_id(db, price.shop_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'shop id:{price.shop_id} not found')
    _price = price.dict()
    _price['book_slug'] = book_slug
    db_price = BookPriceModel(**_price)
    db.add(db_price)
    db.commit()

    return db_price


def create_shop(db: Session, shop: schemas.ShopIn):
    if _is_shop_by_name(db, shop.name):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='shop already created')
    db_shop = ShopModel(**shop.dict())
    db.add(db_shop)
    db.commit()
    return db_shop


def get_shops(db: Session):
    return db.query(ShopModel).all()


@decorators.check_slug_book
def create_shop_book(db: Session, book_slug: str,
                     shop_book: schemas.ShopBookIn):
    if not _is_shop_by_id(db, shop_book.shop_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'shop id: {shop_book.shop_id} not found')

    if _is_shop_book(db, book_slug, shop_book.shop_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='relation already created')

    _shop_book = shop_book.dict()
    _shop_book['book_slug'] = book_slug
    db_shop_book = ShopBooksModel(**_shop_book)
    db.add(db_shop_book)
    db.commit()

    return db_shop_book


@decorators.check_slug_book
def get_shop_books(db: Session, book_slug):
    q = db.query(ShopBooksModel).filter(ShopBooksModel.book_slug == book_slug)
    return q.all()


def create_book_parser(db: Session, book):

    if _is_book(db, book.slug):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='book already created')

    if not _is_shop_by_name(db, book.shop_info.shop_name):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='shop not found')
    _ret = None
    _book = book.dict()
    _shop_info = _book.pop('shop_info')
    _shop_info['book_slug'] = book.slug

    shop_name = _shop_info.pop('shop_name')
    shop = db.query(ShopModel).filter(ShopModel.name == shop_name).first()
    _shop_info['shop_id'] = shop.id

    db_book = BookModel(**_book)
    db_shop_info = ShopBooksModel(**_shop_info)
    db.add(db_book)
    db.add(db_shop_info)
    db.commit()

    _ret = schemas.BookOut.from_orm(db_book).dict()
    _ret['shop_info'] = schemas.ShopBookOut.from_orm(db_shop_info).dict()

    return _ret


def _get_all_prices(db: Session, book_slug):
    q = db.query(BookPriceModel).filter(BookPriceModel.book_slug == book_slug)
    return q.all()


def _is_shop_by_id(db: Session, shop_id: int):
    q = db.query(ShopModel).filter(ShopModel.id == shop_id).exists()
    return db.query(q).scalar()


def _is_shop_by_name(db: Session, shop_name: str):
    q = db.query(ShopModel).filter(ShopModel.name == shop_name).exists()
    return db.query(q).scalar()


def _is_shop_book(db: Session, book_slug, shop_id):
    q = db.query(ShopBooksModel).filter(
        and_(
            ShopBooksModel.book_slug == book_slug,
            ShopBooksModel.shop_id == shop_id)
    ).exists()

    return db.query(q).scalar()


def _is_book(db, book_slug):
    q = db.query(BookModel).filter(BookModel.slug == book_slug).exists()
    return db.query(q).scalar()
