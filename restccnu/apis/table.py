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
def api_get_table(s, sid):
    xnm = request.args.get('xnm')
    xqm = request.args.get('xqm')

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
def api_add_table(s, sid):
    if request.method == 'POST':
        user = connection.User.find_one({'sid': sid})
        if user is None:
            return jsonify({}), 404

        course = request.get_json().get('course')
        teacher = request.get_json().get('teacher')
        weeks = request.get_json().get('weeks')
        day = request.get_json().get('day')
        start = request.get_json().get('start')
        during = request.get_json().get('during')
        place = request.get_json().get('place')
        remind = request.get_json().get('remind')
        id = request.get_json().get('id')
        new_json = {'course': course, 'teacher': teacher, 'weeks': weeks,
                    'day': day, 'start': start, 'during': during,
                    'place': place, 'remind': remind, 'id': id}
        table = user['table']
        table.append(new_json)
        user['table'] = table;
        user.save()

        return jsonify({}), 201


@api.route('/table/<int:id>/', methods=['DELETE'])
@require_info_login
def api_delete_table(s, sid, id):
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
