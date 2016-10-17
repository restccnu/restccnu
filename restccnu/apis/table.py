# coding: utf-8
"""
    table.py
    `````````

    华师匣子课表API模块
"""

import base64
import redis
import json
from flask import request, jsonify, current_app
from .decorators import require_info_login, tojson
from . import api
from ..spiders.table import get_table
from ..spiders.login import info_login
from restccnu.errors import ForbiddenError, NotfoundError
from restccnu.models import connection, User, _zero  # 占位课程(id=0)


@api.route('/table/')
@require_info_login
@tojson
def api_get_table(s, sid):
    """
    :function: api_get_table
    :args:
        - s: 爬虫session对象
        - sid: 学号 

    模拟登录信息门户、获取课表
    """
    xnm = current_app.config['XNM']
    xqm = current_app.config['XQM']

    rv = get_table(s, sid, xnm, xqm)
    user = connection.User.find_one({'sid': sid})
    if user is None:
        u = connection.User()
        u['sid'] = sid; u['table'] = [_zero]
        u.save()
    user = connection.User.find_one({'sid': sid})

    infocourse_dict = []
    for index, course in enumerate(rv):
        course.update({'color': index - 4*(index//4)})
        infocourse_dict.append(course)

    return user['table'] + infocourse_dict


@api.route('/table/', methods=['POST'])
@require_info_login
def api_add_table(s, sid):
    """
    :function: api_add_table
    :args:
        - s: 爬虫session对象
        - sid: 学号

    添加自定义课程, 存储mongodb数据库
    """
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
                    'place': place, 'remind': remind, 'id': id, 'color': 0}
        table = user['table']
        for item in table:
            if item.get('id') == str(id):
                return jsonify({'bad request':
                                'id already exist in database'}), 400
        table.append(new_json)
        user['table'] = table;
        user.save()

        return jsonify({}), 201


@api.route('/table/<int:id>/', methods=['DELETE'])
@require_info_login
def api_delete_table(s, sid, id):
    """
    :function: api_delete_table
    :args:
        - s: 爬虫session对象
        - sid: 学号
        - id: 对应课表本地存储(客户端缓存)的id

    删除课程
    """
    if request.method == 'DELETE':
        user = connection.User.find_one({'sid': sid})
        if user is None:
            return jsonify({}), 404
        table = user['table']
        for i, item in enumerate(table):
            if item.get('id') == str(id):
                del table[i]
        user.save()
        return jsonify({}), 200
