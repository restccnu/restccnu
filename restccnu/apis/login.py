# coding: utf-8

from restccnu.spiders.login import info_login, lib_login
from . import api
from flask import jsonify
from restccnu.errors import ForbiddenError


@api.route('/info/login/')
def mock_info_login():
    try:
        s = info_login()  # 获取信息门户登录句柄
    except ForbiddenError as e:
        return jsonify({}), e.status_code
    else:
        return jsonify({}), 200


@api.route('/lib/login/')
def mock_lib_login():
    try:
        s = lib_login()  # 获取图书馆登录句柄
    except ForbiddenError as e:
        return jsonify({}), e.status_code
    else:
        return jsonify({}), 200
