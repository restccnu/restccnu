# coding: utf-8

import json
import requests
from bs4 import BeautifulSoup
from flask import request
from . import table_test_url
from . import table_index_url
from . import link_index_url


def get_table(s, sid, xnm, xqm):
    """
    s: 信息门户登录操作句柄
    """
    test_url = table_test_url
    table_url = table_index_url % sid
    link_url = link_index_url
    post_data = {'xnm': xnm, 'xqm': xqm}
    s.get(link_url)
    r = s.post(table_url, post_data)
    json_data = r.json()
    kbList = json_data.get('kbList')
    kcList = []
    for item in kbList:
        _item_dict = dict({
            'course': item.get('kcmc'),
            'teacher': item.get('xm'),
            'weeks': item.get('zcd'),
            'day': item.get('xqjmc'),
            'during': item.get('jcs'),
            'place': item.get('xqmc') + item.get('cdmc')})
        kcList.append(_item_dict)
    return kcList
