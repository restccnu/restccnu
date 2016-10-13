# coding: utf-8

import json
from test_basic import APITestCase


class APITestELE(APITestCase):
    def test_api_ele(self):
        """[INFO]->电费查询"""
        resp = self.client.post(
            '/api/ele/',
            headers = self.get_api_headers('', ''),
            data = json.dumps({
                "dor": "东16-419",
                "type": "light"
            })
        )
        self.assertEqual(resp.status_code, 200)

    def test_api_ele_dor_noexist(self):
        """[INFO]->电费查询寝室不存在"""
        resp = self.client.post(
            '/api/ele/',
            headers = self.get_api_headers('', ''),
            data = json.dumps({
                "dor": "东16-4190",
                "type": "light"
            })
        )
        self.assertEqual(resp.status_code, 404)
