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


@api.route('/calendar/', methods=['GET'])
def get_calendar():
    """
    get calendar, key value
    {'calendars': 'imgfilename'}
    """
    if not rds.get('calendars'):
        return jsonify({}), 404
    else:
        calendar = rds.get('calendars')
        try:
            update = qiniu.info(calendar)['putTime']
        except KeyError:
            update = qiniu.info(calendar)
        return jsonify({
            "img": qiniu.url(calendar),
            "update": update,
        }), 200


@api.route('/calendar/', methods=['POST'])
@admin_required
def new_calendar():
    """
    add a new calendar
    """
    if request.method == 'POST':
        img = request.get_json().get('img')

        # store in banners hash list
        rds.set('calendars', img)
        rds.bgsave()

        return jsonify({}), 201
