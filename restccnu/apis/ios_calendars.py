# coding: utf-8
"""
    ios::calendars.py
    `````````````````

    校历API::IOS版

    :MAINTAINER: neo1218
    :OWNER: muxistudio
"""

import json
from . import api
from .. import rds, qiniu
from .decorators import admin_required
from flask import jsonify, request


# placeholder
rds.hset('ios_calendars', '_placeholder', '_placeholder')


@api.route('/ios/calendar/', methods=['GET'])
def get_ios_calendar():
    """ (ios版)
    :function: get_ios_calendar
    :args: none
    :rv: calendar json info

    redis1(6384):
        key: <calendar name>-<qiniu resource name>
        value: size

    返回校历信息
    """
    if rds.hlen('ios_calendars') == 1:
        return jsonify({}), 404
    else:
        calendar = rds.hgetall('ios_calendars')
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


@api.route('/ios/calendar/', methods=['POST'])
@admin_required
def new_ios_calendar():
    """ (ios版)
    :function: new_ios_calendar
    :args: none
    :rv: json message

    上传一个新的校历
    """
    if request.method == 'POST':
        img = request.get_json().get('img')
        size = request.get_json().get('size')

        calendar = rds.hgetall('ios_calendars')
        for filename in calendar:
            if filename != '_placeholder':
                rds.hdel('ios_calendars', filename)
        rds.hset('ios_calendars', img, size)
        rds.save()

        return jsonify({}), 201
