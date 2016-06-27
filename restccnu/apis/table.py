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
    user = connection.User.find_one({'sid': sid})
    return user['table']


@api.route('/table/', methods=['POST'])
@require_info_login
def api_add_table(s):
    if request.method == 'POST':
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
        id = request.get_json().get('id')
        new_json = {'course': course,
                    'teacher': teacher,
                    'weeks': weeks,
                    'day': day,
                    'during': during,
                    'place': place,
                    'id': id}

        table = user['table']
        table.append(new_json)
        user['table'] = table;
        user.save()

        return jsonify({}), 201


@api.route('/table/<int:id>/', methods=['DELETE'])
@require_info_login
def api_delete_table(s, id):
    hashstr = request.headers.get('Authorization')
    base64_hashstr = hashstr[6:]
    id_password = base64.b64decode(base64_hashstr)
    sid, password = id_password.split(':')

    if request.method == 'DELETE':
        user = connection.User.find_one({'sid': sid})
        if user is None:
            return jsonify({}), 404
        table = user['table']
        for i, item in enumerate(table):
            if item.get('id') == str(id):
                del table[i]
        user['table'] = table
        user.save()
        return jsonify({}), 200

