# coding: utf-8

from test_basic import APITestCase


class APIIndexTest(APITestCase):
    def test_api_index(self):
        """test->华师匣子API v1"""
        resp = self.client.get(
                '/api/',
                headers = self.get_api_headers('', '')
        )
        self.assertEqual(resp.status_code, 200)
