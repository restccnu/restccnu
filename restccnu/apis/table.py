# coding: utf-8

import base64
import redis
import json
from flask import request, jsonify
from .decorators import require_info_login, tojson
from . import api
from ..spiders.table import get_table
from ..spiders.login import info_login
from restccnu.errors import ForbiddenError, NotfoundError
from restccnu.models import connection


@api.route('/table/')
@require_info_login
@tojson
def api_get_table(s):
    xnm = request.args.get('xnm')
    xqm = request.args.get('xqm')
    # sid = request.args.get('sid')
    hashstr = request.headers.get('Authorization')
    base64_hashstr = hashstr[6:]
    id_password = base64.b64decode(base64_hashstr)
    sid, password = id_password.split(':')

    rv = get_table(s, sid, xnm, xqm)
    user = connection.User.find_one({'sid': sid})
    if user is None:
        u = connection.User()
        u['sid'] = sid; u['table'] = rv
        u.save()
    # user['table'] = rv
    # user.save()
    return user['table']


@api.route('/table/', methods=['POST'])
@require_info_login
def api_add_table(s):
    if request.method == 'POST':
        # xnm = request.get_json().get('xnm')
        # xqm = request.get_json().get('xqm')
        hashstr = request.headers.get('Authorization')
        base64_hashstr = hashstr[6:]
        id_password = base64.b64decode(base64_hashstr)
        sid, password = id_password.split(':')

        user = connection.User.find_one({'sid': sid})
        if user is None:
            return jsonify({}), 404

        course = request.get_json().get('course')
        teacher = request.get_json().get('teacher')
        weeks = request.get_json().get('weeks')
        day = request.get_json().get('day')
        during = request.get_json().get('during')
        place = request.get_json().get('place')
        new_json = {'course': course,
                    'teacher': teacher,
                    'weeks': weeks,
                    'day': day,
                    'during': during,
                    'place': place}

        table = user['table']
        table.append(new_json)
        user['table'] = table;
        user.save()

        return jsonify({}), 201
