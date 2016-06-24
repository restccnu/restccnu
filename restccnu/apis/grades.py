# coding: utf-8

from . import api
from .decorators import require_info_login, tojson
from ..spiders.grade import get_grade
from flask import request


@api.route('/grade/search/')
@tojson
@require_info_login
def api_get_grade(s):
    sid = request.args.get('sid')
    xnm = request.args.get('xnm')
    xqm = request.args.get('xqm')
    return get_grade(s, sid, xnm, xqm)
