# coding: utf-8

from . import api
from .decorators import require_info_login, tojson
from ..spiders.grade import get_grade, get_grade_detail
from flask import request, current_app


@api.route('/grade/search/')
@tojson
@require_info_login
def api_get_grade(s, sid):
    xnm = request.args.get('xnm')
    xqm = request.args.get('xqm')
    # xnm = current_app.config['XNM']
    # xqm = current_app.config['XQM']
    return get_grade(s, sid, xnm, xqm)


@api.route('/grade/detail/search/')
@tojson
@require_info_login
def api_get_detail_grade(s, sid):
    xnm = request.args.get('xnm')
    xqm = request.args.get('xqm')
    # xnm = current_app.config['XNM']
    # xqm = current_app.config['XQM']
    course = request.args.get('course')
    jxb_id = request.args.get('jxb_id')
    return get_grade_detail(s, sid, xnm, xqm, course, jxb_id)
