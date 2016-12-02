# coding: utf-8

import json
import requests
from bs4 import BeautifulSoup
from . import headers, proxy


def get_ele(meter, dor, typeit):
    """
    :function: get_ele
    :args:
        - meter: 电表号
        - dor: 宿舍号
        - typeit: 电费类别
            - light: 照明🔦
            - air: 空调🈳
    :rv:
        电费查询信息

    :V2.0: 2.0版新接口爬虫, 欢迎加入restccnu的爬虫大家庭
    """
    ele_url = "http://jnb.ccnu.edu.cn/weixin/example/demo/search.php"
    if meter == 0:
        return {'dor': dor,
            'degree': {
                'remain': "",
                'before': "",
                'current': "", },
            'ele': {
                'remain': "",
                'before': "",
                'current': "", }
        }
    else:
        # set cookie
        cookies = {'ammeterid': meter}
        r = requests.get(ele_url, cookies=cookies)
        html = r.content
        soup = BeautifulSoup(html, 'lxml', from_encoding='utf-8')

        degree_before = str(soup.find_all('div', class_="weui_cell_bd weui_cell_primary"))
        degree_current = ""
        degree_remain = ""

        ele_before = ""
        ele_current = ""
        ele_remain = ""

        return {
            'dor': dor,
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
