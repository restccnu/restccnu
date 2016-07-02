# coding: utf-8
# meter_index file

import os
import requests
from bs4 import BeautifulSoup


html_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'htmls'))
"""
==> meter_index 格式
meter_index = {
    'x1101': ['29275', '2'], 'x1102': ['29276', '3'], 'x1103': ['29277', '4'],
}
"""
_meter_index = {}
def colour_meter_index():
    for dirs, subdirs, files in os.walk(html_path):
        for file in files:
            file_path = os.path.join(html_path, file)
            soup = BeautifulSoup(open(file_path), 'lxml')
            options = soup.find('tr', id='MeterDiv').find_all('option')
            _key_value = []
            for option in options:
                key = option.get('value').split('*')[-2][:-2]
                value = option.get('value').split('*')[0]
                if key in _meter_index.keys():
                    _meter_index[key].append(value)
                else:
                    _meter_index[key] = [value]
        return _meter_index
