# coding: utf-8

import requests
import base64
from flask import request
from restccnu.errors import ForbiddenError
from . import info_login_url
from . import info_login_test_url
from . import lib_login_url
from . import lib_login_test_url
from . import headers


# Authorization: Basic base64(sid:password)
def info_login():
    LoginUrl = info_login_url
    TestUrl = info_login_test_url 

    hashstr = request.headers.get('Authorization')
    base64_hashstr = hashstr[6:]
    id_password = base64.b64decode(base64_hashstr)
    sid, password = id_password.split(':')

    # for test
    s = requests.Session()
    s.post(LoginUrl, {
        'userName': sid, 'userPass': password
    }), headers

    r = s.get(TestUrl)
    if 'window.alert' in r.content:
        raise ForbiddenError
    else:
        return s


# Authorization: Basic base64(sid:password)
def lib_login():
    LoginUrl = lib_login_url
    TestUrl = lib_login_test_url

    hashstr = request.headers.get('Authorization')
    base64_hashstr = hashstr[6:]
    id_password = base64.b64decode(base64_hashstr)
    sid, password = id_password.split(':')

    s = requests.Session()
    s.post(LoginUrl, {
        'number': sid, 'passwd': password, 'select': 'cert_no'
    }), headers

    r = s.get(TestUrl)
    if '123456' in r.content:
        raise ForbiddenError
    else:
        return s
