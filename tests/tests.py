import random
from datetime import datetime as dt
from datetime import timedelta
import unittest
import copy

from .base import BaseAPITest
from .data import shop_data, book_data, shop_book_data, price_data

from fastapi import status


class ShopsTest(BaseAPITest):
    def test_create_one_shop(self):
        _shop_data = copy.deepcopy(shop_data)

        response = self.create_shop(shop_data)
        _shop_data['id'] = dict(response.json()).get('id')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), _shop_data)

        response = self.get_shops()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [_shop_data, ])

    def test_create_many_shops(self):
        _shops_data = []

        for i in range(1, 5):
            _data = copy.deepcopy(shop_data)
            _data['name'] = _data['name'].join(str(i))
            response = self.create_shop(_data)

            _data['id'] = dict(response.json()).get('id')
            _shops_data.append(_data)

        response = self.get_shops()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), _shops_data)

    def test_create_duplicate_shop(self):
        response = self.create_shop(shop_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.create_shop(shop_data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        error_detail = {'detail': 'shop already created'}
        self.assertEqual(response.json(), error_detail)


class BookTest(BaseAPITest):
    def test_create_one_book(self):
        response = self.create_book(book_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), book_data)

        response = self.get_books()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [book_data, ])

        response = self.get_book_info(book_data['slug'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), book_data)

    def test_create_many_books(self):
        _books_data = []
        for i in range(1, 5):
            _data = copy.deepcopy(book_data)
            _data['slug'] = _data['slug'].join(str(i))
            self.create_book(_data)
            _books_data.append(_data)

        response = self.get_books()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), _books_data)

    def test_create_duplicate_book(self):
        response = self.create_book(book_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.create_book(book_data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        error_detail = {'detail': 'book already created'}
        self.assertEqual(response.json(), error_detail)


class ShopBookTest(BaseAPITest):
    def test_create_one_shop_book(self):
        book_slug, _shop_book_data = self._create_shop_and_book(
            book_data,
            shop_data,
            shop_book_data)

        response = self.create_shop_books(book_slug, _shop_book_data)
        _shop_book_data['id'] = dict(response.json()).get('id')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), _shop_book_data)

        response = self.get_shop_books(book_slug)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [_shop_book_data])

    def test_create_many_shop_books(self):
        _data = []
        _shop_book_data = copy.deepcopy(shop_book_data)
        _shop_data = copy.deepcopy(shop_data)

        response = self.create_book(book_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        for i in range(1, 5):
            response = self.create_shop(_shop_data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            _shop_book_data['shop_id'] = dict(response.json()).get('id')

            response = self.create_shop_books(book_data['slug'],
                                              _shop_book_data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            _data.append(response.json())
            _shop_data['name'] = 'shop_name_'.join(str(i))

        response = self.get_shop_books(book_data['slug'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), _data)

    def test_create_duplicat_shop_books(self):
        book_slug, _shop_book_data = self._create_shop_and_book(book_data,
                                                                shop_data,
                                                                shop_book_data)

        response = self.create_shop_books(book_slug, _shop_book_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.create_shop_books(book_slug, _shop_book_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        error_detail = {'detail': 'relation already created'}
        self.assertEqual(response.json(), error_detail)

    def test_create_shop_book_without_book(self):
        _shop_book_data = copy.deepcopy(shop_book_data)
        response = self.create_shop(shop_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        _shop_book_data['shop_id'] = dict(response.json()).get('id')
        fake_slug = 'fake_slug'
        response = self.create_shop_books(fake_slug, _shop_book_data)
        error_detail = {'detail': 'book not found'}
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), error_detail)

    def test_create_shop_book_without_shop(self):
        _shop_book_data = copy.deepcopy(shop_book_data)
        response = self.create_book(book_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        _shop_book_data['shop_id'] = random.randint(1, 120000)
        book_slug = dict(response.json()).get('slug')
        response = self.create_shop_books(book_slug, _shop_book_data)
        error_detail = {
            'detail': f'shop id:{_shop_book_data["shop_id"]} not found'
        }
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), error_detail)

    def _create_shop_and_book(self, b_data, s_data, s_b_data):
        _shop_book_data = copy.deepcopy(s_b_data)
        response = self.create_shop(s_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        _shop_book_data['shop_id'] = dict(response.json()).get('id')

        response = self.create_book(b_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        book_slug = dict(response.json()).get('slug')
        _shop_book_data['book_slug'] = book_slug

        return [book_slug, _shop_book_data]


class PricesTest(BaseAPITest):
    def test_create_one_price(self):
        _shop_data = copy.deepcopy(shop_data)
        _price_data = copy.deepcopy(price_data)
        response = self.create_book(book_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        book_slug = dict(response.json()).get('slug')

        response = self.create_shop(_shop_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        _price_data['shop_id'] = dict(response.json()).get('id')

        response = self.create_price(book_slug, _price_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        _price_data['id'] = dict(response.json()).get('id')
        _price_data['date'] = dict(response.json()).get('date')
        self.assertEqual(response.json(), _price_data)

    def test_create_many_prices(self):
        _shop_data = copy.deepcopy(shop_data)
        _price_data = copy.deepcopy(price_data)
        _ret_data = []
        response = self.create_book(book_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        book_slug = dict(response.json()).get('slug')

        response = self.create_shop(_shop_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        _price_data['shop_id'] = dict(response.json()).get('id')

        for i in range(1, 5):
            response = self.create_price(book_slug, _price_data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            _element = copy.deepcopy(_price_data)
            _element['id'] = dict(response.json()).get('id')
            _ret_data.append(_element)
            _price_data['price'] = random.randint(4, 10000)

        response = self.get_prices(book_slug)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for element in response.json():
            _ret_data[element['id'] - 1]['date'] = element['date']

        self.assertEqual(response.json(), _ret_data)

        params = {'last_prices': True}
        response = self.get_prices_last(book_slug, params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [_ret_data[-1], ])


# class ParserTest(BaseAPITest):
#     def test_create_one_book(self):
#         _book_parser_data = copy.deepcopy(book_data)
#
#         response = self.create_shop(shop_data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         _shop_book_data = copy.deepcopy(shop_book_data)
#         _shop_book_data['shop_name'] = dict(response.json()).get('name')
#         _book_parser_data['shop_info'] = _shop_book_data
#         shop_id = dict(response.json()).get('id')
#
#         response = self.create_book_parser(_book_parser_data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         _book_parser_data['shop_info']['id'] = dict(
#             response.json()).get('shop_info').get('id')
#         _ = _book_parser_data['shop_info'].pop('shop_name')
#         _book_parser_data['shop_info']['book_slug'] = _book_parser_data['slug']
#         _book_parser_data['shop_info']['shop_id'] = shop_id
#
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(response.json(), _book_parser_data)
#
#         response = self.get_book_info(_book_parser_data['slug'])
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.json(), book_data)
#
#     def test_create_book_no_shop(self):
#         _book_parser_data = copy.deepcopy(book_data)
#
#         _shop_book_data = copy.deepcopy(shop_book_data)
#         _shop_book_data['shop_name'] = str([chr(random.randint(1, 10)) for _ in range(10)])
#         _book_parser_data['shop_info'] = _shop_book_data
#
#         response = self.create_book_parser(_book_parser_data)
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#         error_detail = {
#             'detail': 'shop not found'
#         }
#         self.assertEqual(response.json(), error_detail)
#
#     def test_create_book_already_created(self):
#         _book_parser_data = copy.deepcopy(book_data)
#         response = self.create_shop(shop_data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         _shop_book_data = copy.deepcopy(shop_book_data)
#         _shop_book_data['shop_name'] = dict(response.json()).get('name')
#         _book_parser_data['shop_info'] = _shop_book_data
#
#         response = self.create_book(book_data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#
#         response = self.create_book_parser(_book_parser_data)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         error_detail = {
#             'detail': 'book already created'
#         }
#         self.assertEqual(response.json(), error_detail)


if __name__ == '__main__':
    unittest.main()
