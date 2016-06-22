# coding: utf-8

import requests
from bs4 import BeautifulSoup


def get_table(s):
    """
    s: 信息门户登录操作句柄
    """
    test_url = "http://portal.ccnu.edu.cn/index_jg.jsp"
    table_url = "http://122.204.187.6/kbcx/xskbcx_cxXsKb.html"
    post_data = {'xnm': '2015', 'xqm': '3'}
    # r = s.post(table_url, post_data)
    r = s.get(test_url)
    return r.content
