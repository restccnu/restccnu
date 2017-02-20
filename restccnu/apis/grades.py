# coding: utf-8
"""
    grades.py
    `````````

    成绩查询API

    :MAINTAINER: neo1218
    :OWNER: muxistudio
"""

from . import api
from .decorators import require_info_login, tojson
from ..spiders.grade import get_grade, get_grade_detail
from flask import request, current_app


@api.route('/grade/search/')
@require_info_login
@tojson
def api_get_grade(s, sid):
    """
    :function: api_get_grade
    :args:
        - s: 爬虫session
        - sid: 学号
    :rv: json

    总成绩查询
    """
    xnm = request.args.get('xnm')
    xqm = request.args.get('xqm')
    grade_list = get_grade(s, sid, xnm, xqm)
    for _course in grade_list:
        name = _course.get('course')
        jxb_id = _course.get('jxb_id')
        grade_detail = get_grade_detail(s, sid, xnm, xqm, name, jxb_id)
        _course.update(grade_detail)
    return grade_list


@api.route('/grade/detail/search/')
@require_info_login
@tojson
def api_get_detail_grade(s, sid):
    """
    :function: api_get_detail_grade
    :args:
        - s: 爬虫session
        - sid: 学号
    :rv: json

    平时成绩查询

    20161017:
        平时成绩查询学校已不提供此项功能.
        此API将在第二版中移除
    """
    xnm = request.args.get('xnm')
    xqm = request.args.get('xqm')
    course = request.args.get('course')
    jxb_id = request.args.get('jxb_id')
    return get_grade_detail(s, sid, xnm, xqm, course, jxb_id)
