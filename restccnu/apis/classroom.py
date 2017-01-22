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


def update_each(table):
    """
    :function: update_each
    :args:
        - table: 课表

    根据每个年级的课表更新空闲教室表
    """
    # 将每天对应的节次设定为空列表
    def init_weekdays(weekday_list):
        for sec in range(1, 15):
            weekday_list['%d' % sec] = list()

    # 初始化每周每天对应的字典
    def init_week(week_name):
        week = connection.Week()
        week['weekNo'] = week_name
        week['mon'] = dict()
        week['tue'] = dict()
        week['wed'] = dict()
        week['thu'] = dict()
        week['fri'] = dict()
        init_weekdays(week['mon'])
        init_weekdays(week['tue'])
        init_weekdays(week['wed'])
        init_weekdays(week['thu'])
        init_weekdays(week['fri'])
        week.save()
        sys.stdout.write('%r initialiezed!' % week_name)

    rows_count = table.nrows
    for count in range(rows_count):
        values = table.row_values(rows_count)
        times = values[:3]    # 上课时间 1-3
        val_locations = values[3:]    # 上课地点 1-3
        locations = list(str(int(each)) for each in val_locations if isinstance(each, float))
        for time in times:
            # 上课的星期
            weekday = time[time.index(u'\u671f')+1]
            # 上课的节次
            sec_li = list(int(i) for i in time[time.index(u'\u7b2c')+1:time.index(u'\u8282')].split('-'))
            secs = range(sec_li[0], sec_li[1]+1)
            # 上课的周次
            week_li = list(int(i) for i in time[time.index('{')+1:time.index(u'\u5468')].split('-'))

            # 根据单双周筛选上课的周数
            if u'\u5355' in time:
                do_weeks = list(each for each in range(week_li[0], week_li[1]+1) if each%2!=0)
            if u'\u53cc' in time:
                do_weeks = list(each for each in range(week_li[0], week_li[1]+1) if each%2==0)
            else:
                do_weeks = list(each for each in range(week_li[0], week_li[1]+1))

            # 将教室添加到对应周对应星期对应的节次
            for do_week in do_weeks:
                week = connection.Week.find_one({'weekNo': 'week%d' % do_week})
                if weekday == u'\u4e00':
                    do_weekday = week['mon']
                elif weekday == u'\u4e8c':
                    do_weekday = week['tue']
                elif weekday == u'\u4e09':
                    do_weekday = week['wed']
                elif weekday == u'\u56db':
                    do_weekday = week['thu']
                elif weekday == u'\u4e94':
                    do_weekday = week['fri']
                for each_sec in secs:
                    do_weekday['%d' % each_sec].extend(locations)
                week.save()
        sys.stdout.write('row %r handled!' % count)



@api.route('/classroom/update/', methods=['POST'])
@admin_required
def api_update_classroom():
    """
    :function: api_update_classroom
    :args: none

    更新空闲教室表(上传课表时需将无关行列删除)
    """
    if request.method == 'POST':
        table_path = os.environ.get('TABLE_PATH')
        data = xlrd.open_workbook(table_path)
        all_tables = data.sheets()
        try:
            for each_table in all_tables:
                update_each(each_table)
            return jsonify({}), 200
        except:
            return jsonify({}), 500


@api.route('/classroom/get/')
def api_get_classrooom(s, sid):
    """
    :function: api_get_classroom
    :args:
        - s: 爬虫session对象
        - sid: 学号

    获取空闲教室表
    """
    user = connection.User.find_one({'sid': sid})
    if user is None:
        return jsonify({}), 403
