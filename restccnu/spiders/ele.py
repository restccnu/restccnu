# coding: utf-8
"""
    ele.py
    ``````

    电费信息爬虫

    :MAINTAINER: neo1218
    :OWNER: muxistudio
"""

import json
import requests
import HTMLParser
from bs4 import BeautifulSoup
from flask import jsonify
from . import headers, proxy
from . import ele_url, new_ele_url

html_parser = HTMLParser.HTMLParser()

def get_old_ele(meter, dor, typeit):
    """
    -> 旧电费接口爬虫
    """
    post_data = {
            "nodeInText": "%s*Meter" % meter,
            "PartList": "",
            "SelectPart": 1}
    r = requests.post(
        ele_url, data=json.dumps(post_data),
        headers={'Content-Type': 'application/json'},
        proxies=proxy, timeout=7
    )
    content = r.json()
    main_html = content.get('d').split('|')[1].replace('', '')
    parse_html = html_parser.unescape(main_html)
    html = '<html><body>' + parse_html + '</body></html>'

    soup = BeautifulSoup(html, 'lxml', from_encoding='utf-8')

    divMeterTopBox = soup.find('div', id='divMeterTopBox')
    divMeterTopBoxtrs = divMeterTopBox.tr.next_siblings

    _tr_dict = {}; _key = 0
    for tr in divMeterTopBoxtrs:
        _key += 1
        _tr_dict.update({str(_key): tr})

    _ele = float(_tr_dict['4'].td.next_sibling.text[:-1])

    if typeit == 'light':
        ele_remain = float(divMeterTopBox.find('td', id='tdSYValue').text[:-1])
        degree_remain = "%.2f" % (ele_remain / _ele)
    elif typeit == 'air':
        degree_remain = float(divMeterTopBox.find('td', id='tdSYValue').text[:-1])
        ele_remain = "%.2f" % (degree_remain * _ele)

    ele_before = _tr_dict['2'].td.next_sibling.text.split('：')[1][:-2]
    ele_current = _tr_dict['3'].td.next_sibling.text.split('：')[1][:-2]

    degree_before = _tr_dict['2'].td.next_sibling.text.split('(')[0][:-3]
    degree_current = _tr_dict['3'].td.next_sibling.text.split('(')[0][:-3]

    return {
        'dor': dor,
        'degree': {
             'remain': degree_remain,
             'before': degree_before,
             'current': degree_current,
        },
        'ele': {
             '_ele': _ele,
             'remain': ele_remain,
             'before': ele_before,
             'current': ele_current,
        }
    }


def get_new_ele(meter, dor, typeit):
    """
    -> 新电费接口爬虫
    """
    # set cookie
    cookies = {'ammeterid': meter}
    r = requests.get(new_ele_url, cookies=cookies, timeout=7, proxies=proxy)
    html = r.content
    soup = BeautifulSoup(html, 'lxml', from_encoding='utf-8')

    all_p = soup.find_all("p")
    _ele = float(all_p[5].strings.next()[:-2])

    degree_current = ""
    for ch in all_p[4].strings.next():
        try:
            int(ch); degree_current += ch
        except ValueError:
            if ch == '.': degree_current += '.'
    degree_before = ""
    for ch in all_p[3].strings.next():
        try:
            int(ch); degree_before += ch
        except ValueError:
            if ch == '.': degree_before += '.'

    ele_before = ""
    for ch in list(all_p[3].strings)[1]:
        try:
            int(ch); ele_before += ch
        except ValueError:
            if ch == '.': ele_before += '.'
    ele_current = ""
    for ch in list(all_p[4].strings)[1]:
        try:
            int(ch); ele_current += ch
        except ValueError:
            if ch == '.': ele_current += ch

    if typeit == 'light':
        ele_remain = float(all_p[7].strings.next()[:-2])
        degree_remain = "%.2f" % (ele_remain / _ele)
    elif typeit == 'air':
        degree_remain = float(all_p[7].strings.next()[:-4])
        ele_remain = "%.2f" % (degree_remain * _ele)

    return {
        'dor': dor,
        '_ele': _ele,
        'degree': {
            'remain': degree_remain,
            'before': degree_before,
            'current': degree_current,
        },
        'ele': {
            'remain': ele_remain,
            'before': ele_before,
            'current': ele_current
        }
    }   


def get_ele(meter, dor, typeit):
    """
    :function: get_ele
    :args:
        - meter: 电表号
        - dor: 宿舍号
        - typeit: 电费类别
            - light: 照明
            - air: 空调
    :rv:

    查询电费信息

    :V2.0: 换了新接口爬虫(ele.py), 这个爬虫已经死了(哀伤)
           😢  新接口同样恶心, 所以这里爬虫还要继续用...
           🍄  决定2个接口一起爬...
    """
    if meter == 0:
        return {'dor': dor,
            'degree': {
                'remain': "",
                'before': "",
                'current': "", },
            'ele': {
                '_ele': "",
                'remain': "",
                'before': "",
                'current': "",
            }
        }
    else:
        try:
            return get_old_ele(meter, dor, typeit)
        except requests.exceptions.Timeout:
            try:
                return get_new_ele(meter, dor, typeit)
            except requests.exceptions.Timeout:
                return jsonify({}), 500
