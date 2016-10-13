# coding: utf-8

import os
import json
from test_basic import APITestCase


class APITestBanner(APITestCase):
    def test_api_banner(self):
        """[INFO]->获取banner API"""
        resp = self.client.get(
            '/api/banner/',
            headers = self.get_api_headers('', '')
        )
        # 返回404表示没有banner
        self.assertEqual(resp.status_code, 200)

    def test_api_banner_add(self):
        """[INFO]->添加banner"""
        resp = self.client.post(
            '/api/banner/',
            headers = self.get_api_headers(
                os.getenv('ADMIN_EMAIL'),
                os.getenv('ADMIN_PASS')
            ),
            data = json.dumps({
                'img': 'http://7xj431.com1.z0.glb.clouddn.com/ic-xueer.png',
                'url': 'https://xueer.muxixyz.com'
            })
        )
        self.assertEqual(resp.status_code, 201)

    def test_api_banner_add_noadmin(self):
        """[INFO]->添加banner权限"""
        resp = self.client.post(
            '/api/banner/',
            headers = self.get_api_headers(
                "我很随便", "<.<我也很随便"
            ),
            data = json.dumps({
                'img': '0_thumb.jpg',
                'url': 'https://xueer.muxixyz.com'
            })
        )
        self.assertEqual(resp.status_code, 401)

    def test_api_banner_delete(self):
        """[INFO]->删除banner"""
        resp = self.client.delete(
            '/api/banner/?name=0_thumb.jpg',
            headers = self.get_api_headers(
                os.getenv("ADMIN_EMAIL"),
                os.getenv("ADMIN_PASS")
            )
        )
        self.assertEqual(resp.status_code, 200)
