from .base import BaseAPITest
from .data import shop_data, book_data, book_url_data
from fastapi import status
import unittest
import copy


class ShopsTest(BaseAPITest):
    def test_create_one_shop(self):
        response = self.create_shop(shop_data)

        _shop_data = copy.deepcopy(shop_data)
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

    def test_create_one_book_for_url(self):
        response = self.create_shop(shop_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.create_book(book_url_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), book_url_data)

        response = self.get_books()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [book_data, ])

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

    def test_create_duplicate_shop(self):
        response = self.create_book(book_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.create_book(book_data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        error_detail = {'detail': 'book already created'}
        self.assertEqual(response.json(), error_detail)


if __name__ == '__main__':
    unittest.main()
