# coding: utf-8

import redis
import json
from flask import request, jsonify
from .decorators import require_info_login, tojson
from . import api
from ..spiders.table import get_table
from ..spiders.login import info_login
from restccnu.errors import ForbiddenError
from restccnu import rds


@api.route('/table/')
@require_info_login
@tojson
def api_get_table(s):
    xnm = request.args.get('xnm')
    xqm = request.args.get('xqm')
    sid = request.args.get('sid')
    rv = get_table(s, sid, xnm, xqm)
    # rv = rds.get(sid) if rds.get(sid) else get_table(s, sid, xnm, xqm)
    # rv = list(rv) if isinstance(rv, unicode) else rv
    return rv


@api.route('/table/', methods=['POST'])
@require_info_login
def api_add_table(s):
    if request.method == 'POST':
        sid = request.get_json().get('sid')
        xnm = request.get_json().get('xnm')
        xqm = request.get_json().get('xqm')
        rv = get_table(s, sid, xnm, xqm)
        json_data = json.dumps(rv, indent=1, ensure_ascii=False)

        course = request.get_json().get('course')
        teacher = request.get_json().get('teacher')
        weeks = request.get_json().get('weeks')
        day = request.get_json().get('day')
        during = request.get_json().get('during')
        place = request.get_json().get('place')

        new_json = {
                'course': course,
                'teacher': teacher,
                'weeks': weeks,
                'day': day,
                'during': during,
                'place': place}

        data = json_data
        rds.set(sid, data)
        rds.save()
        return jsonify({})
