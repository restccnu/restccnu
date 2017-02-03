# coding: utf-8
"""
    meter_index.py
    ``````````````

    宿舍电表号爬虫

    :MAINTAINER: neo1218
    :OWNER: muxistudio
"""

import os
import requests
from bs4 import BeautifulSoup


html_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'htmls'))


def colour_meter_index():
    """
    :function: colour_meter_index

    生成寝室```电表表:)```
    """
    _meter_index = {}
    for dirs, subdirs, files in os.walk(html_path):
        for file in files:
            file_path = os.path.join(html_path, file)
            soup = BeautifulSoup(open(file_path), 'lxml')
            options = soup.find('tr', id='MeterDiv').find_all('option')
            _key_value = []
            for option in options:
                if file[0] not in ['d', 's', 'x', 'y', 'n', 'c']:
                    # 国交
                    building = file[0]
                    key = option.get('value').split('*')[-2]
                    if '国' not in key:
                        if (("空调" in key) or ("照明" in key)):
                            key = u'国' + building + '-' + key[:-2]
                        else: key = u'国' + building + '-' + key
                elif file[0] == 'c':
                    # 产宿
                    key = option.get('value').split('*')[-2][:-2]
                    if '-' in key:
                        _key = key.split('-')
                        if len(_key[-1]) == 1:
                            _key[-1] = "0"+_key[-1]
                        key = (_key[0][0]+_key[0][-1]) + '-' + _key[1][:-1] + _key[-1]
                elif file[0] == 's':
                    # 南湖
                    # 南湖有的寝室没有空调(((ﾟДﾟ;)))
                    key = option.get('value').split('*')[-2]
                    if (("空调" in key) or ("照明" in key)):
                        key = key[:-2]
                else:
                    # 其他寝室
                    key = option.get('value').split('*')[-2][:-2]  # dor
                    if "新增" in key:
                        key = key.replace(u"新增", "")
                    elif "新" in key:
                        key = key.replace(u"新", "")
                value = option.get('value').split('*')[0]          # meter
                if key in _meter_index.keys():
                    _meter_index[key].append(value)
                else:
                    _meter_index[key] = [value]
        return _meter_index
