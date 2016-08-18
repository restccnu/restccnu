# coding: utf-8

"""
    static.py
    `````````

    静态资源API, 使用七牛存储服务
    Flask-Zero
    : https://github.com/neo1218/Flask-Zero
"""

import os
import datetime
from . import api
from .decorators import tojson
from restccnu import qiniu, rds
from qiniu import BucketManager
from flask import request


@api.route('/banner/', methods=['post', 'get'])
@tojson
def get_banner():
    json_data = []
    banners = eval(rds.get('banners') or '[]')
    for banner_dict in banners:
        filename = banner_dict.keys()[0]
        if filename:
            update_timestamp = qiniu.info(filename).get('putTime')
            json_data.append({
                'filename': filename,
                'img': qiniu.url(filename),
                'url': banner_dict.get(filename),
                'update': update_timestamp,
                'size': qiniu.info(filename).get('fsize'),
                'info': qiniu.info(filename)
            })
        else:
            json_data.append({})
    return json_data


@api.route('/calendar/', methods=['post', 'get'])
@tojson
def get_calendar():
    json_data = []
    calendars = eval(rds.get('calendars') or '[]')
    for calendar_dict in calendars:
        filename = calendar_dict.keys()[0]
        size = calendar_dict.get(filename)
        if filename:
            update_timestamp = qiniu.info(filename).get('putTime')
            json_data.append({
                'filename': filename,
                'img': qiniu.url(filename),
                'update': update_timestamp,
                'size': size,
            })
        else:
            json_data.append({})
    return json_data


@api.route('/start/', methods=['post', 'get'])
@tojson
def get_start():
    """
    获取闪屏图片
    """
    start = eval(rds.get('start') or '{}')
    if start:
        filename = start.keys()[0]
        url = start.get(filename)
        return {
            'img': qiniu.url(filename),
            'url': url or '',
            'update': qiniu.info(filename).get('putTime')
        }
    else:
        return {}
