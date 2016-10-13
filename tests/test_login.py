# coding: utf-8

import os
from test_basic import APITestCase


class APITestLogin(APITestCase):
    def test_api_login(self):
        """[INFO]->信息门户模拟登录"""
        resp = self.client.get(
            '/api/info/login/',
            headers = self.get_api_headers(
                os.getenv("USER_NAME"),
                os.getenv("USER_PASS")
            )
        )
        self.assertEqual(resp.status_code, 200)

    def test_api_login_noauth(self):
        """[INFO]->信息门户模拟登录验证错误"""
        resp=self.client.get(
            '/api/info/login/',
            headers = self.get_api_headers(
                "我不是朱承浩",
                "你就是朱承浩好不好...不要这么无聊..."
            )
        )
        self.assertEqual(resp.status_code, 403)
