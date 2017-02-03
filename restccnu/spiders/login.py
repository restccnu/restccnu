# coding: utf-8
"""
    login.py
    ````````

    模拟登录爬虫
        - 图书馆
        - 信息门户

    :MAINTAINER: neo1218
    :OWNER: muxistudio

"""

import time
import gevent
import requests
import base64
from flask import request
from restccnu import rds
from restccnu.errors import ForbiddenError
from . import info_login_url
from . import info_login_test_url
from . import lib_login_url
from . import lib_login_test_url
from . import headers, proxy


# Authorization: Basic base64(sid:password)
def info_login():
    """
    :function: info_login

    模拟登录信息门户
    """
    LoginUrl = info_login_url
    TestUrl = info_login_test_url

    hashstr = request.headers.get('Authorization')
    if hashstr is None:
        raise ForbiddenError()
    base64_hashstr = hashstr[6:]
    id_password = base64.b64decode(base64_hashstr)
    sid, password = id_password.split(':')
      
    # set rds lru cache for speed up resolve nginx header
    # rds:6384 (restccnulru)
    password_hash = base64.b64encode(password)

    s = requests.Session()  # s: 爬虫session对象
    s.post(LoginUrl, {
        'userName': sid, 'userPass': password
    }, headers=headers, proxies=proxy)

    r = s.get(TestUrl)
    if 'window.alert' in r.content:
        raise ForbiddenError()
    else:
        rds.hset('restccnulru', sid, password_hash)
        rds.save()
        return s, sid


# Authorization: Basic base64(sid:password)
def lib_login():
    """
    :function: lib_login

    模拟登录图书馆
    """
    LoginUrl = lib_login_url
    TestUrl = lib_login_test_url

    hashstr = request.headers.get('Authorization')
    if hashstr is None:
        raise ForbiddenError()
    base64_hashstr = hashstr[6:]
    id_password = base64.b64decode(base64_hashstr)
    sid, password = id_password.split(':')

    s = requests.Session()
    s.post(LoginUrl, {
        'number': sid, 'passwd': password, 'select': 'cert_no'
    }, headers=headers, proxies=proxy)

    r = s.get(TestUrl)
    if '123456' in r.content:
        raise ForbiddenError()
    else:
        return s, sid
