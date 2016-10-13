# coding: utf-8

from test_basic import APITestCase

class APITestCalendar(APITestCase):
    def test_api_calendar(self):
        """[INFO]->校历"""
        resp = self.client.get(
            '/api/calendar/',
            headers = self.get_api_headers('', '')
        )
        # 不好意思... 测试没有添加校历
        self.assertEqual(resp.status_code, 404)
