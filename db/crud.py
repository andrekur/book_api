import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, and_

from . import schemas
from .models import BookModel, ShopModel, BookPriceModel, ShopBooksModel


def check_slug_book(func):
    """
    Декоратор для проверки книги по slug
    """
    def wrapper(db, *args, book_slug, **kwargs):
        q = db.query(BookModel).filter(BookModel.slug == book_slug).exists()

        if not db.query(q).scalar():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='book not found')

        return func(db, *args, book_slug=book_slug, **kwargs)
    return wrapper


def check_shop(func):
    """
    Декоратор для проверки магазина по name, id
    """
    def wrapper(db, *args, shop_id=None, shop_name=None, **kwargs):
        if shop_id is not None:
            if not _is_shop_by_id(db, shop_id):
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=f'shop id:{shop_id} not found')
        elif shop_name is not None:
            if not _is_shop_by_name(db, shop_name):
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=f'shop name:{shop_name} not found')
        else:
            raise Exception(f'shop_id and shop_name is None')
        return func(db, *args, **kwargs)
    return wrapper


@check_slug_book
def get_book(db: Session, book_slug: str,):
    """
    book_slug: slug книги

    Получить конкретную книгу

    return: BookModel
    """
    q = db.query(BookModel).filter(BookModel.slug == book_slug)
    return q.first()


def get_books(db: Session):
    """
    Получить все книги

    return: BookModel
    """
    return db.query(BookModel).all()


def create_book(db: Session, book: schemas.BookIn):
    """
    book: BookIn

    Создать книгу

    return: BookModel
    """
    q = db.query(BookModel).filter(BookModel.slug == book.slug).exists()
    if db.query(q).scalar():
        raise HTTPException(status_code=404, detail='book already created')

    db_book = BookModel(**book.dict())
    db.add(db_book)
    db.commit()
    return db_book


@check_slug_book
def get_book_prices(db: Session, last_prices: bool, book_slug: str):
    """
    last_prices: bool  Найти только последнюю цену для каждого магазина
    book_slug: slug книги

    Найти все цены для книги

    return: BookPriceModel
    """
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


@check_shop
@check_slug_book
def create_book_prices(db: Session,
                       price: schemas.PriceIn,
                       book_slug):
    """
    price: PriceIn
    book_slug: slug книги

    Создать новую цену на книгу в магазине

    return: BookPriceModel
    """
    _price = price.dict()
    _price['book_slug'] = book_slug
    _price['date'] = datetime.datetime.now()
    db_price = BookPriceModel(**_price)
    db.add(db_price)
    db.commit()

    return db_price


def create_shop(db: Session, shop: schemas.ShopIn):
    """
    shop: ShopIn

    Создать магазин

    return: ShopModel
    """
    if _is_shop_by_name(db, shop.name):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='shop already created')
    db_shop = ShopModel(**shop.dict())
    db.add(db_shop)
    db.commit()
    return db_shop


def get_shops(db: Session):
    """
    Получить все магазины

    return: ShopModel
    """
    return db.query(ShopModel).all()


@check_shop
@check_slug_book
def create_shop_book(db: Session,
                     shop_book: schemas.ShopBookIn,
                     book_slug: str):
    """
    book_slug: slug книги
    shop_book: ShopBookIn

    Создать ссылку на книгу в магазине
    (Связать книгу-магазин-ссылка_на_книгу)

    return: ShopBookModel
    """

    if _is_shop_book(db, book_slug, shop_book.shop_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='relation already created')

    _shop_book = shop_book.dict()
    _shop_book['book_slug'] = book_slug
    db_shop_book = ShopBooksModel(**_shop_book)
    db.add(db_shop_book)
    db.commit()

    return db_shop_book


@check_slug_book
def get_shop_books(db: Session, book_slug):
    """
    book_slug: slug книги

    Получить все ссылки на книгу

    return: ShopBookModel
    """
    q = db.query(ShopBooksModel).filter(ShopBooksModel.book_slug == book_slug)
    return q.all()


def create_book_parser(db: Session, book):
    """
    Функция для парсера
    Добавляет книгу, если книга есть то добавляет новую цену
    """

    if not _is_shop_by_name(db, book['shop_info']['shop_name']):
        raise Exception(f"shop:{book['shop_info']['shop_name']} not found")

    _shop_info = book.pop('shop_info')
    _price_info = book.pop('price_info', None)
    shop_name = _shop_info.pop('shop_name')
    shop = db.query(ShopModel).filter(ShopModel.name == shop_name).first()

    if _is_book(db, book['slug']):
        if not _price_info:
            raise Exception(f"book_slug: {book['slug']} book already created, price_info is None")
        __parser_create_price(db, book['slug'], shop.id, _price_info)
        return

    _shop_info['book_slug'] = book['slug']
    _shop_info['shop_id'] = shop.id

    db_book = BookModel(**book)
    db_shop_info = ShopBooksModel(**_shop_info)

    db.add(db_book)
    db.add(db_shop_info)
    db.commit()

    if _price_info:
        __parser_create_price(db, book['slug'], shop.id, _price_info)


def _get_all_prices(db: Session, book_slug):
    """
    book_slug: slug книги

    Получить все цены на книгу

    return: все цены на книгу
    """
    q = db.query(BookPriceModel).filter(BookPriceModel.book_slug == book_slug)
    return q.all()


def _is_shop_by_id(db: Session, shop_id: int) -> bool:
    """
    shop_id: id магазина

    Проверить существование магазина по его id

    return: bool
    """
    q = db.query(ShopModel).filter(ShopModel.id == shop_id).exists()
    return db.query(q).scalar()


def _is_shop_by_name(db: Session, shop_name: str) -> bool:
    """
    shop_name: название магазина
    Проверить существование магазина по его name

    return: bool
    """
    q = db.query(ShopModel).filter(ShopModel.name == shop_name).exists()
    return db.query(q).scalar()


def _is_shop_book(db: Session, book_slug, shop_id) -> bool:
    """
    book_slug: slug книги
    shop_id: id магазина

    Проверить есть ли связь магазин книга

    return: bool
    """
    q = db.query(ShopBooksModel).filter(
        and_(
            ShopBooksModel.book_slug == book_slug,
            ShopBooksModel.shop_id == shop_id)
    ).exists()

    return db.query(q).scalar()


def _is_book(db, book_slug) -> bool:
    """
    book_slug: slug книги

    Проверить есть ли книга с таким  slug

    return: bool
    """
    q = db.query(BookModel).filter(BookModel.slug == book_slug).exists()
    return db.query(q).scalar()


def __parser_create_price(db, book_slug, shop_id, price_info) -> None:
    """
    book_slug: slug книги
    shop_id: id магазина
    price_info: информация о цене

    Добавить цену книге с таким slug и shop_id

    return: None
    """
    price_info['date'] = datetime.datetime.now()
    price_info['book_slug'] = book_slug
    price_info['shop_id'] = shop_id
    db_price = BookPriceModel(**price_info)
    db.add(db_price)
    db.commit()
