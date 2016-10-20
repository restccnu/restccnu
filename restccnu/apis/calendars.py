# coding: utf-8
"""
    calendars.py
    ````````````

    校历API

    :MAINTAINER: neo1218
    :OWNER: muxistudio
"""

import json
from . import api
from .. import rds, qiniu
from .decorators import admin_required
from flask import jsonify, request


# placeholder
rds.hset('calendars', '_placeholder', '_placeholder')


@api.route('/calendar/', methods=['GET'])
def get_calendar():
    """
    :function: get_calendar
    :args: none
    :rv: calendar json info

    redis1(6384):
        key: <calendar name>-<qiniu resource name>
        value: size

    返回校历信息
    """
    if rds.hlen('calendars') == 1:
        return jsonify({}), 404
    else:
        calendar = rds.hgetall('calendars')
        for filename in calendar:
            if filename != '_placeholder':
                try:
                    update = qiniu.info(filename)['putTime']
                except KeyError:
                    update = qiniu.info(filename)
                return jsonify({
                    "img": qiniu.url(filename),
                    "filename": filename,
                    "update": update,
                    'size': calendar.get(filename),
                }), 200


@api.route('/calendar/', methods=['POST'])
@admin_required
def new_calendar():
    """
    :function: new_calendar
    :args: none
    :rv: json message

    上传一个新的校历
    """
    if request.method == 'POST':
        img = request.get_json().get('img')
        size = request.get_json().get('size')

        calendar = rds.hgetall('calendars')
        for filename in calendar:
            if filename != '_placeholder':
                rds.hdel('calendars', filename)
        rds.hset('calendars', img, size)
        rds.save()

        return jsonify({}), 201
