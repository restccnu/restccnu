# coding: utf-8

"""
    login.py
    ````````

    : info_login 信息门户登录:
    : lib_login 校图书馆登录:
"""

import requests
import base64


headers = {
    'User-Agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:45.0) Gecko/20100101 Firefox/45.0",
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    'Accept-Language':"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    'Accept-Encoding':"gzip, deflate",
}


# Authorization: Basic base64(sid:password)
def info_login():
    LoginUrl = "http://portal.ccnu.edu.cn/loginAction.do"
    TestUrl = "http://portal.ccnu.edu.cn/chpass.jsp"

    hashstr = requests.headers.get('Authorization')
    base64_hashstr = hashstr[6:]
    id_password = base64.b64decode(base64_hashstr)
    sid, password = id_password.split(':')

    s = requests.Session()
    s.post(LoginUrl {
        'userName': sid, 'userPass': password
    }), headers

    r = s.get(TestUrl)
    if 'window.alert' in r.content:
        return "403"
    else:
        return s # isinstance(s, requests.Session)
