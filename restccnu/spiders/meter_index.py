# coding: utf-8
# meter_index file

import os
import requests
from bs4 import BeautifulSoup


html_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'htmls'))


meter_index = {
    'x1101': ['29275', '2'], 'x1102': ['29276', '3'], 'x1103': ['29277', '4'],
    'x1104': ['29278', '5'], 'x1105': ['', '6'], 'x1106': ['29279', '7'],
    'x1107': ['29280', '8'], 'x1108': ['29281', '9'], 'x1109': ['29282', '10'],
    'x1110': ['29283', '11'], 'x1111': ['29284', '12'], 'x1112': ['29285', '13'],
    'x1113': ['29286', '14'], 'x1114': ['29287', '15'], 'x1115': ['29288', '16'],
    'x1116': ['29289', '17'], 'x1117': ['29290', '18'], 'x1118': ['29291', '19'],
    'x1119': ['29292', '20'], 'x1120': ['29293', '21'], 'x1121': ['29294', '22'],
    'x1122': ['29295', '23'], 'x1123': ['29296', '24'], 'x1124': ['29297', '25'],
    'x1126': ['29298', '26']
}


_meter_index = {}
def colour_meter_index():
    for dirs, subdirs, files in os.walk(html_path):
        # for file in files:
        file_path = os.path.join(html_path, files[0])
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


if __name__ == '__main__':
    print colour_meter_index()
