# coding: utf-8

import os
from test_basic import APITestCase


class APITestLib(APITestCase):
    def test_api_lib_search(self):
        """[INFO]->图书查询"""
        resp = self.client.get(
            "/api/lib/search/?keyword=python&page=1",
            headers = self.get_api_headers('', '')
        )
        self.assertEqual(resp.status_code, 200)

    def test_api_lib_detail(self):
        """[INFO]->图书详情"""
        resp = self.client.get(
            "/api/lib/?id=0001309040&book=1.Python数据分析&author=(印尼) Ivan Idris著&bid=fff",
            headers = self.get_api_headers('', '')
        )
        self.assertEqual(resp.status_code, 200)

    def test_api_lib_me(self):
        """[INFO]->我的图书馆"""
        resp = self.client.get(
            "/api/lib/me/",
            headers = self.get_api_headers(
                os.getenv("USER_NAME"),
                "123456"
            )
        )
        self.assertEqual(resp.status_code, 200)

    def test_api_lib_me_noauth(self):
        """[INFO]->我的图书馆用户名或密码错误"""
        resp = self.client.get(
            "/api/lib/me/",
            headers = self.get_api_headers(
                "我不是朱承浩",
                "123456"
            )
        )
        self.assertEqual(resp.status_code, 403)
