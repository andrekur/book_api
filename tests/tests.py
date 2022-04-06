from .base import BaseAPITest
from .data import shop_data
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

    def test_create_many_shop(self):
        _shops_data = []
        for i in range(2, 5):
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


if __name__ == '__main__':
    unittest.main()
