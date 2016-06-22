# coding: utf-8

import requests
from bs4 import BeautifulSoup


def get_table(s):
    """
    s: 信息门户登录操作句柄
    """
    table_url = "http://122.204.187.6/kbcx/xskbcx_cxXsKb.html"
    post_data = {'xnm': '2015', 'xqm': '3'}
    r = s.post(table_url, post_data)
    return r.content

# 现在存在登录超时的问题
