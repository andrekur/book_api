from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class BookShop(BaseModel):
    shop_id: int
    url: str


class _BookBase(BaseModel):
    slug: str
    name: str
    count_pages: str
    weight: str
    size: str

    class Config:
        orm_mode = True


class BookIn(_BookBase):
    shop: Optional[BookShop] = None


class BookOut(_BookBase):
    id: int


class Price(BaseModel):
    id: int
    price: int
    discount_price: int
    shop_id: int
    date: datetime

    class Config:
        orm_mode = True


class _ShopBase(BaseModel):
    name: str

    class Config:
        orm_mode = True


class ShopIn(_ShopBase):
    pass


class ShopOut(_ShopBase):
    id: int
