# coding: utf-8

import json
import requests
from bs4 import BeautifulSoup
from flask import request


# GET /hzsflogin?ticket=wKhQEg0HHcVxIOBR7SNX5P6GHET6CICDV9TW HTTP/1.1
# http://122.204.187.6/hzsflogin?ticket=wKhQEg0HHcVxIOBR7SNX5P6GHET6CICDV9TW
# http://122.204.187.6/xtgl/login_tickitLogin.html <== GET Cookie
def get_table(s, sid, xnm, xqm):
    """
    s: 信息门户登录操作句柄
    """
    test_url = "http://portal.ccnu.edu.cn/index_jg.jsp"
    table_url = "http://122.204.187.6/kbcx/xskbcx_cxXsKb.html?" + \
                "gnmkdmKey=N253508&sessionUserKey=%s" % sid
    link_url = "http://portal.ccnu.edu.cn/roamingAction.do?appId=XK"
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
            # 'start': item.get('')
            # 'during':
            'during': item.get('jcs'),
            'place': item.get('xqmc') + item.get('cdmc')})
        kcList.append(_item_dict)
    return kcList
# start ~ during
# database: id
