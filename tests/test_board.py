# coding: utf-8

from test_basic import APITestCase

class APITestBoard(APITestCase):
    def test_api_board(self):
        """[INFO]->通知公告"""
        resp = self.client.get(
            '/api/info/',
            headers = self.get_api_headers('', '')
        )
        self.assertEqual(resp.status_code, 200)
