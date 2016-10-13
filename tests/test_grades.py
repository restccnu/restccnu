# coding: utf-8

import os
from test_basic import APITestCase


class APITestGrades(APITestCase):
    def test_api_grade(self):
        """[INFO]->总成绩查询"""
        resp = self.client.get(
            '/api/grade/search/?xnm=2015&xqm=3',
            headers = self.get_api_headers(
                os.getenv('USER_NAME'),
                os.getenv('USER_PASS')
            )
        )
        self.assertEqual(resp.status_code, 200)
