# coding: utf-8
"""
    table.py
    `````````

    华师匣子课表API模块

    :MAINTAINER: neo1218
    :OWNER: muxistudio
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
from restccnu.models import connection, User, Table, _zero  # 占位课程(id=0)


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

    v1.0.3: ~用户可以删除信息门户课表
    """
    xnm = current_app.config['XNM']
    xqm = current_app.config['XQM']

    rv = get_table(s, sid, xnm, xqm)
    user = connection.User.find_one({'sid': sid})
    if user is None:
        u = connection.User()
        u['sid'] = sid; u['table'] = [_zero]  # mongodb占位
        u.save()
    user = connection.User.find_one({'sid': sid})
    # 从数据库中读取信息门户课表
    table = connection.Table.find_one({'sid': sid})
    if table is None:
        # 第一次获取table的时候, 将
        # 信息门户中的课程数据写入数据库, 并添加id
        infocourse_list = []
        for index, course in enumerate(rv):
            course.update({'color': index-4*(index//4)})
            course.update({'id': str(1024+index)})
            infocourse_list.append(course)
        u = connection.Table()
        u['sid'] = sid; u['table'] = infocourse_list
        u.save()
    table = connection.Table.find_one({'sid': sid})

    # 返回: 用户自定义课程 + 信息门户课程
    return user['table'] + table['table']


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


@api.route('/ios/table/', methods=['POST'])
@require_info_login
def api_ios_add_table(s, sid):
    """
    api_ios_add_table: 
        课表添加ios临时接口
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
        # id = request.get_json().get('id')
        table = user['table']
        item_id = [int(item.get('id')) for item in table]
        max_id = max(item_id)
        id = str(max_id + 1)
        new_json = {'course': course, 'teacher': teacher, 'weeks': weeks,
                    'day': day, 'start': start, 'during': during,
                    'place': place, 'remind': remind, 'id': id, 'color': 0}
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

    v1.0.3: ~用户可以删除信息门户课表
    """
    if request.method == 'DELETE':
        if id < 1024:
            user = connection.User.find_one({'sid': sid})
            if user is None:
                return jsonify({}), 404
            tables = user['table']
            for i, item in enumerate(tables):
                if item.get('id') == str(id):
                    del tables[i]
                user.save()
            return jsonify({}), 200
        else:
            table = connection.Table.find_one({'sid': sid})
            if table is None:
                return jsonify({}), 404
            tables = table['table']
            for i, item in enumerate(tables):
                if item.get('id') == str(id):
                    del tables[i]
                table.save()
            return jsonify({}), 200

@api.route('/table/<int:id>/', methods=['PUT', 'GET'])
@require_info_login
def api_edit_table(s, sid, id):
    """
    :function: api_edit_table
    :args:
        - id: 待修改的课程的id

    修改指定id的课程(用户自定义课程, 信息门户课程)
    """
    if request.method == 'PUT':
        course = request.get_json().get("course")
        teacher = request.get_json().get("teacher")
        weeks = request.get_json().get("weeks")
        day = request.get_json().get("day")
        start = request.get_json().get("start")
        during = request.get_json().get("during")
        place = request.get_json().get("place")
        remind = request.get_json().get("remind")

        courses = connection.User.find_one({'sid': sid}) if id < 1024 else \
                  connection.Table.find_one({'sid': sid})
        tables = courses['table']; _course = None
        for i, item in enumerate(tables):
            if item.get('id') == str(id):
                _course = tables[i]
        if _course is None:
            return jsonify({}), 404
        _course['course'] = course; _course['teacher'] = teacher
        _course['weeks'] = weeks; _course['day'] = day
        _course['start'] = start; _course['during'] = during
        _course['place'] = place; _course['remind'] = remind
        ## update _course
        courses['table'] = tables
        courses.save()
    return jsonify({}), 200
