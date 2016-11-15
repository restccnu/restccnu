# coding: utf-8
"""
    table.py
    ````````

    课表爬虫

    :MAINTAINER: neo1218
    :OWNER: muxistudio
"""

import random
import json
import requests
from bs4 import BeautifulSoup
from flask import request
from . import table_test_url
from . import table_index_url
from . import link_index_url
from . import headers, proxy


def get_table(s, sid, xnm, xqm):
    """
    :function: get_table
    :args:
        - s: 爬虫session对象
        - sid: 学号
        - xnm: 学年
        - xqm: 学期

    信息门户课表爬虫
    """
    test_url = table_test_url
    table_url = table_index_url % sid
    link_url = link_index_url
    post_data = {'xnm': xnm, 'xqm': xqm}
    s.get(link_url, headers=headers, proxies=proxy)
    r = s.post(table_url, post_data, headers=headers)
    json_data = r.json()
    kbList = json_data.get('kbList'); kcList = []; weeks_list = []
    for item in kbList:
        _weeks = item.get('zcd')
        if '(' in _weeks:
            weeks =  _weeks.split('(')
            time = weeks[0]; mode = weeks[-1]
            if ',' in time:
                times = time.split(',')
                weeks_list.append(times[0][:-1])
                time = times[1]
            _time = time.split('-')
            _start = int(_time[0]); _last = int(_time[-1][:-1])
            if mode:
                weeks_list = range(_start, _last+1, 2)
        elif ',' in _weeks:
            weeks = _weeks.split(','); weeks_list = []
            for week in weeks:
                if '-' in week:
                    _start = int(week.split('-')[0])
                    _last = int(week.split('-')[1][:-1])
                    _weeks_list = range(_start, _last+1)
                    weeks_list += _weeks_list
                else:
                    weeks_list.append(week[:-1])
        elif '-' in _weeks: 
            weeks = _weeks.split('-')
            _start = int(weeks[0]); _last = int(weeks[-1][:-1])
            weeks_list = range(_start, _last+1)
        else:
            weeks_list = [int(_weeks[:-1])]
        str_weeks_list = [str(i) for i in weeks_list]
        _class = item.get('jcs').split('-')
        s_class = int(_class[0]); e_class = int(_class[-1])
        d_class = e_class - s_class + 1
        _item_dict = dict({
            'course': item.get('kcmc'),
            'teacher': item.get('xm'),
            'weeks': ','.join(str_weeks_list),
            'day': item.get('xqjmc'),
            'start': s_class,
            'during': d_class,
            'place': item.get('xqmc') + item.get('cdmc'),
            'remind': False})
        kcList.append(_item_dict)
    return kcList
