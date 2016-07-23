# coding: utf-8

"""
    static.py
    `````````

    静态资源API, 使用七牛存储服务
    Flask-QiniuStorage
"""

import os
from . import api
from .decorators import tojson
from restccnu import qiniu, rds
from flask import request


@api.route('/banner/', methods=['post', 'get'])
@tojson
def get_banner():
    json_data = []
    banners = eval(rds.get('banners'))
    for banner_dict in banners:
        filename = banner_dict.keys()[0]
        json_data.append({
                'filename': filename,
                'img': qiniu.url(filename),
                'url': banner_dict.get(filename),
                'update': '2016-07-22' })
    return json_data


@api.route('/calendar/', methods=['post', 'get'])
@tojson
def get_calendar():
    json_data = []
    calendars = eval(rds.get('calendars'))
    for calendar_dict in calendars:
        filename = calendar_dict.keys()[0]
        json_data.append({
                'filename': filename,
                'img': qiniu.url(filename),
                'update': '2016-07-22' })
    return json_data
