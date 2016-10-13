# coding: utf-8

from test_basic import APITestCase
from flask import url_for
from restccnu.spiders.apartment import _apartment_list


class APITestApartment(APITestCase):
    def test_api_apartment(self):
        """test->部门信息"""
        resp = self.client.get(
            # url_for('api.api_get_apartment'),
            '/api/apartment/',
            headers=self.get_api_headers('', '')
        )
        self.assertEqual(eval(resp.data), _apartment_list)

    
