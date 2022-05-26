from pydantic import BaseModel
from datetime import datetime


class BookShop(BaseModel):
    id: int
    url: str


class _BookBase(BaseModel):
    slug: str
    name: str
    count_pages: int
    weight: int
    size: str

    class Config:
        orm_mode = True


class BookIn(_BookBase):
    pass


class BookOut(_BookBase):
    pass


class _ShopBase(BaseModel):
    name: str

    class Config:
        orm_mode = True


class ShopIn(_ShopBase):
    pass


class ShopOut(_ShopBase):
    id: int


class _BaseShopBook(BaseModel):
    shop_id: int
    url: str

    class Config:
        orm_mode = True


class ShopBookIn(_BaseShopBook):
    pass


class ShopBookOut(_BaseShopBook):
    id: int
    book_slug: str


class _BasePrice(BaseModel):
    price: int
    discount_price: int

    class Config:
        orm_mode = True


class PriceIn(_BasePrice):
    shop_id: int
    pass


class PriceOut(_BasePrice):
    id: int
    date: datetime
    shop_id: int


class _ParserShopBook(BaseModel):
    shop_name: str
    url: str

    class Config:
        orm_mode = True


class ParserBookIn(_BookBase):
    shop_info: _ParserShopBook
    price_info: _BasePrice = None


class ParserBookOut(BookOut):
    shop_info: ShopBookOut
