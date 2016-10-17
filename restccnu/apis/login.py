# coding: utf-8
"""
    login.py
    `````````

    模拟登录API模块

    :MAINTAINER: neo1218
    :OWNER: muxistudio
"""

from . import api
from flask import jsonify
from .decorators import require_info_login, require_lib_login


@api.route('/info/login/')
@require_info_login
def api_info_login(s, sid):
    """
    :function: api_info_login
    :args:
        - s: 爬虫session对象
        - sid: 学号
    :rv: json message
    
    模拟登录信息门户API
    """
    return jsonify({}), 200


@api.route('/lib/login/')
@require_lib_login
def api_lib_login(s, sid):
    """
    :function: api_lib_login
    :args:
        - s: 爬虫session对象
        - sid: 学号
    :rv: json message

    模拟登录图书馆API
    """
    return jsonify({}), 200
