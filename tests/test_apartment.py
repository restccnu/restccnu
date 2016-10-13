# coding: utf-8

from test_basic import APITestCase
from flask import url_for
from restccnu.spiders.apartment import _apartment_list


class APITestApartment(APITestCase):
    def test_api_apartment(self):
        """test apartment api"""
        resp = self.client.get(
            # url_for('api.api_get_apartment'),
            '/api/apartment/',
            headers=self.get_api_headers('', '')
        )
        self.assertEqual(eval(resp.data), _apartment_list)

    def test_api_index(self):
        resp = self.client.get(
            '/api/',
            headers = self.get_api_headers('', '')
        )
        self.assertEqual(resp.status_code, 200)
