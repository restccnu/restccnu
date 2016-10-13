# coding: utf-8

import os
import json
from test_basic import APITestCase


class APITestProduct(APITestCase):
    def test_api_product(self):
        """[INFO]->木犀产品展示API"""
        resp = self.client.get(
            '/api/product/',
            headers = self.get_api_headers('', ''),
        )
        # 502: 服务器端异常
        self.assertEqual(resp.status_code, 200)

    def test_api_product_update(self):
        """[INFO]->添加木犀展示产品"""
        resp = self.client.put(
            '/api/product/',
            headers = self.get_api_headers(
                os.getenv('ADMIN_EMAIL'),
                os.getenv('ADMIN_PASS')
            ),
            data = json.dumps({
                "name": "xueer",
                "icon": "http://7xj431.com1.z0.glb.clouddn.com/ic-xueer.png",
                "url": "https://xueer.muxixyz.com",
                "intro": u"华师课程经验挖掘机"
            })
        )
        self.assertEqual(resp.status_code, 200)

    def test_api_product_update_noadmin(self):
        """[INFO]->添加木犀展示产品权限"""
        resp = self.client.put(
            '/api/product/',
            headers = self.get_api_headers(
                "我很随便", "<.<我也很随便"
            ),
            data = json.dumps({
                "name": "xueer",
                "icon": "http://7xj431.com1.z0.glb.clouddn.com/ic-xueer.png",
                "url": "https://xueer.muxixyz.com",
                "intro": u"华师课程经验挖掘机"
            })
        )
        self.assertEqual(resp.status_code, 401)

    def test_api_product_delete(self):
        """[INFO]->删除木犀展示产品"""
        resp = self.client.delete(
            '/api/product/?name=xueer',
            headers = self.get_api_headers(
                os.getenv('ADMIN_EMAIL'),
                os.getenv('ADMIN_PASS')
            )
        )
        self.assertEqual(resp.status_code, 200)
