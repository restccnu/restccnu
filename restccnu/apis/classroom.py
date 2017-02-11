# -*- coding: utf-8 -*-
"""
    classroom.py
    ````````

    空闲教室API

    :MAINTAINER: kasheemlew
    :OWNER: muxistudio
"""

import os
import sys
import json
import xlrd
from . import api
from flask import request, jsonify
from .decorators import tojson, admin_required
from restccnu.models import connection, Week


@api.route('/classroom/get_classroom/', methods=['GET'])
def api_get_classrooom():
    """
    :function: api_get_classroom
    :args: none

    获取空闲教室表
    """
    weekno = request.args.get('weekno')
    weekday = request.args.get('weekday')
    building = request.args.get('building')

    try:
        week = connection.Week.find_one({'weekNo': unicode('week'+weekno), 'bno': unicode(building)})
        classroom_list = week[weekday]
        return jsonify(classroom_list)
    except:
        return jsonify({}), 502
