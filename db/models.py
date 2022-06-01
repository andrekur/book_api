from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, UniqueConstraint

from .connector import Base


class BookModel(Base):
    __tablename__ = 'books'

    slug = Column(String, primary_key=True, index=True)
    name = Column(String)
    count_pages = Column(Integer)
    weight = Column(Integer)
    size = Column(String)


class ShopModel(Base):
    __tablename__ = 'shops'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)


class ShopBooksModel(Base):
    __tablename__ = 'shops_books'
    __table_args__ = (
        UniqueConstraint(
            'shop_id', 'book_slug'
        ),
    )

    id = Column(Integer, primary_key=True)
    shop_id = Column(Integer, ForeignKey('shops.id'), index=True, nullable=False)
    book_slug = Column(String, ForeignKey('books.slug'), index=True, nullable=False)
    url = Column(String)


class BookPriceModel(Base):
    __tablename__ = 'books_prices'
    __table_args__ = (
        UniqueConstraint(
            'shop_id', 'book_slug', 'date'
        ),
    )

    id = Column(Integer, primary_key=True)
    price = Column(Integer)
    discount = Column(Integer)
    shop_id = Column(Integer, ForeignKey('shops.id'), index=True, nullable=False)
    book_slug = Column(String, ForeignKey('books.slug'), index=True, nullable=False)
    date = Column(DateTime)
