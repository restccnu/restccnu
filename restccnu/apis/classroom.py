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


@api.route('/classroom/get_classroom/')
def api_get_classrooom():
    """
    :function: api_get_classroom
    :args: none

    获取空闲教室表
    """
    weekno = request.args.get('weekno')
    weekday = request.args.get('weekday')
    building = request.args.get('building')

    try:
        week = connection.Week.find_one({'weekNo': 'week'+weekno, 'bno': building})
        classroom_list = week[weekday]
        return jsonify(classroom_list)
    except:
        return jsonify({}), 502


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
            return jsonify({}), 502


def update_each(table):
    """
    :function: update_each
    :args:
        - table: 课表

    根据每个年级的课表更新空闲教室表
    """
    # 七号楼和八号楼所有的教室
    s_all = ['7101','7102','7103','7104','7105','7106','7107','7108','7109',
             '7201','7202','7203','7204','7205','7206','7207','7208','7209','7211',
             '7301','7302','7303','7304','7305','7306','7307','7308','7309','7311',
             '7401','7402','7403','7404','7405','7406','7407','7408','7409','7410','7411',
             '7501','7503','7505']
    e_all = ['8101','8102','8103','8104','8105','8106','8107','8108','8109',
             '8110','8111','8112','8201','8202','8203','8204','8205','8206',
             '8207','8208','8209','8210','8211','8212','8213','8214','8215',
             '8216','8301','8302','8303','8304','8305','8306','8307','8308',
             '8309','8310','8311','8312','8313','8314','8315','8316','8401',
             '8402','8403','8404','8405','8406','8407','8408','8409','8410',
             '8411','8412','8413','8414','8415','8416','8501','8502','8503',
             '8504','8505','8506','8507','8508','8509','8510','8511','8512',
             '8513','8514','8515','8516','8716','8717']

    def init_weekdays(weekday_list):
        """将每天对应的节次设定为空列表"""
        for sec in range(1, 15):
            weekday_list['%d' % sec] = list()

    def init_week(week_name, bno):
        """初始化每周每天对应的字典"""
        week = connection.Week()
        week['weekNo'] = week_name
        week['bno'] = bno
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
        sys.stdout.write('weekNo: %r bon: %r initialiezed!' % week_name, bno)

    def change_to_free(bno, cm_all):
        """将上课教室表修改为空闲教室表"""
        weekday_list = ['mon', 'tue', 'wed', 'thu', 'fri']
        for week_count in range(1, 21):
            change_week = connection.Week.find_one({'weekNo': 'week%d'%week_count, 'bno': bno})
            for weekday in weekday_list:
                temp_list = cm_all
                for i in change_week[weekday]:
                    temp_list.remove(i)
                change_week[weekday] = temp_list
            change_week.save()

    # 初始化上课教室
    for loc in ['7', '8']:
        for week_count in range(1, 21):
            if not connection.Week.find_one({'weekNo': 'week%d'%week_count, 'bno': loc}):
                init_week = connection.Week()
                init_week('week%d'%week_count, loc)
                init_week.save()

    # 添加所有上课的教室
    rows_count = table.nrows
    for count in range(rows_count):
        values = table.row_values(count)
        times = values[:3]    # 上课时间 1-3
        val_locs = values[3:]    # 上课地点 1-3
        locations = list(str(int(each)) for each in val_locs if isinstance(each, float) and int(each/1000) in [7, 8])
        for time in times:
            # 上课地点为空，跳至下一循环
            if not time: continue
            # 上课的星期
            weekday = time[time.index(u'\u671f')+1]
            # 上课的节次
            sec_li = list(int(i) for i in time[time.index(u'\u7b2c')+1:time.index(u'\u8282')].split('-'))
            secs = range(sec_li[0], sec_li[1]+1)
            # 上课的周次
            week_li = list(int(i) for i in time[time.index('{')+1:time.index(u'\u5468')].split('-'))
            # 单双周筛选
            if u'\u5355' in time:
                weeks = list(each for each in range(week_li[0], week_li[1]+1) if each%2!=0)
            if u'\u53cc' in time:
                weeks = list(each for each in range(week_li[0], week_li[1]+1) if each%2==0)
            else:
                weeks = list(each for each in range(week_li[0], week_li[1]+1))

            # 将教室添加到对应周对应星期对应的节次
            for do_week in weeks:
                if weekday == u'\u4e00':
                    ft_weekday = 'mon'
                elif weekday == u'\u4e8c':
                    ft_weekday = 'tue'
                elif weekday == u'\u4e09':
                    ft_weekday = 'wed'
                elif weekday == u'\u56db':
                    ft_weekday = 'thu'
                elif weekday == u'\u4e94':
                    ft_weekday = 'fri'
                for each_loc in locations:
                    temp_dict = {}
                    bno = each_loc[0]

                    find_week = connection.Week.find_one({'weekNo': 'week%d' do_week, 'bno': each_loc[0]})
                    if not find_week: continue
                    weekdaydict = find_week[ft_weekday]

                    for each_sec in secs:
                        weekdaydict[each_sec].append(each_loc)
                    find_week.save()

        sys.stdout.write('row %r written!' % count)
    sys.stdout.write('all from xls written!')

    # 修改为空闲教室
    change_to_free('7', s_all)
    change_to_free('8', e_all)
