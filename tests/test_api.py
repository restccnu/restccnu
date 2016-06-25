# coding: utf-8

import unittest
import json
import re
from base64 import b64encode
from flask import url_for
from restccnu import create_app


class APITestcase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.debug = True
        self.app.config.update(
            SERVER_NAME = 'localhost:5050',
            debug = True
        )
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def tearDown(self):
        self.app_context.pop()


    def mock_api_headers(self):
        headers = {
            'User-Agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:45.0) Gecko/20100101 Firefox/45.0",
            'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            'Accept-Language':"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            'Accept-Encoding':"gzip, deflate",
        }
        return headers

    def mock_auth_headers(self, sid, password):
        return {
                'Authorization': 'Basic ' + b64encode(
                    (sid + ':' + password).encode('utf-8')
                ).decode('utf-8'),
                'Accept': 'application/json',
                'Content-Type': 'application/json'
        }

    def test_mock_info_login(self):
        res = self.client.get(
            url_for('api.api_info_login'),
            headers = self.mock_auth_headers('2014210761', '1234')
        )
        self.assertTrue(res.status_code == 200)
        res = self.client.get(
            url_for('api.api_info_login'),
            headers = self.mock_auth_headers('2014210761', '124')
        )
        self.assertTrue(res.status_code == 403)


    def test_mock_lib_login(self):
        res = self.client.get(
            url_for('api.api_lib_login'),
            headers = self.mock_auth_headers('2014210761', '123456')
        )
        self.assertTrue(res.status_code == 200)
        res = self.client.get(
            url_for('api.api_lib_login'),
            headers = self.mock_auth_headers('2014210761', '124')
        )
        self.assertTrue(res.status_code == 403)

    def test_lib_search(self):
        res = self.client.get(url_for('api.api_search_books', keyword='python'))
        json_data = res.data  # null :(
        # 'next' in json_data.get('meta')
        # 'last' in json_data.get('meta')
        # 'per_page' in json_data.get('meta')
        self.assertTrue(res.status_code == 400)

