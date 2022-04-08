from typing import Optional
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


class _BaseBookUrl(BaseModel):
    id: int
    url: str


class BookUrlIn(_BaseBookUrl):
    pass


class BookUrlOut(_BaseBookUrl):
    id: int


class _BasePrice(BaseModel):

    price: int
    discount_price: int
    shop_id: int
    date: datetime

    class Config:
        orm_mode = True


class PriceIn(_BasePrice):
    pass


class PriceOut(_BasePrice):
    id: int
