# coding: utf-8

import unittest
import restccnu
import base64
from restccnu import create_app


class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        # self.app.config.update(
        #         # SERVER_NAME = 'http://localhost:5000',
        # )
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def tearDown(self):
        self.app_context.pop()

    def get_api_headers(self, username, password):
        return {
            'Authorization': 'Basic ' + base64.b64encode(
                (username + ':' + password),
            ),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
