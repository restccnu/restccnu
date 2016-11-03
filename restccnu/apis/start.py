# coding: utf-8
"""
    start.py
    ````````

    华师匣子闪屏API

    :MAINTAINER: neo1218
    :OWNER: muxistudio
"""

import json
from . import api
from .. import rds, qiniu
from .decorators import admin_required
from flask import jsonify, request


# placeholder
rds.hset('starts', '_placeholder', '_placeholder')


@api.route('/start/', methods=['GET'])
def get_start():
    """
    :function: get_start

    redis1(6384)
        key: <filename>-<qiniu resource name>
        value: {
            "img": img, "filename": filename,
            "update": 更新时间, "size": 闪屏大小
        }
    hash set

    获取闪屏
    """
    if rds.hlen('starts') == 1:
        return jsonify({}), 404
    else:
        starts = rds.hgetall('starts')
        for filename in starts:
            if filename != '_placeholder':
                try:
                    update = qiniu.info(filename)['putTime']
                except KeyError:
                    update = qiniu.info(filename)
                return jsonify({
                    "img": qiniu.url(filename),
                    "filename": filename,
                    "update": update,
                    "url": starts.get(filename),
                }), 200


@api.route('/start/', methods=['POST'])
@admin_required
def new_start():
    """
    :function: new_start

    更新一个闪屏
    """
    if request.method == 'POST':
        img = request.get_json().get('img')
        url = request.get_json().get('url')

        # store in banners hash list
        # del older before add new
        starts = rds.hgetall('starts')
        for filename in starts:
            if filename != '_placeholder':
                rds.hdel('starts', filename)
        rds.hset('starts', img, url)
        rds.save()

        return jsonify({}), 201
