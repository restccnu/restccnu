# coding: utf-8

"""
    calendars.py
    ````````````

    ccnubox calendar crud
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
    get calendar, key value
    {'calendars': 'imgfilename'}
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
    add a new calendar
    """
    if request.method == 'POST':
        img = request.get_json().get('img')
        size = request.get_json().get('size')

        # store in banners hash list
        rds.hset('calendars', img, size)
        rds.bgsave()

        return jsonify({}), 201
