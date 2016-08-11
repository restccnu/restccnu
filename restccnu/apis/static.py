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
        update_timestamp = qiniu.info(filename).get('putTime')
        #    date = datetime.datetime.fromtimestamp(update_timestamp)
        # updte_time = date.strftime("%Y-%m-%d")
        json_data.append({
                'filename': filename,
                'img': qiniu.url(filename),
                'url': banner_dict.get(filename),
                # 'update': '2016-07-22' })  # 如何获取七牛文件创建的时间呢?
                'update': update_timestamp})
    return json_data


@api.route('/calendar/', methods=['post', 'get'])
@tojson
def get_calendar():
    json_data = []
    calendars = eval(rds.get('calendars') or '[]')
    for calendar_dict in calendars:
        filename = calendar_dict.keys()[0]
        update_timestamp = qiniu.info(filename).get('putTime')
        json_data.append({
                'filename': filename,
                'img': qiniu.url(filename),
                'update': update_timestamp })
    return json_data
