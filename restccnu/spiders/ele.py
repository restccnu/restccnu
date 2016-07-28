# coding: utf-8
#
import json
import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:45.0) Gecko/20100101 Firefox/45.0",
    'Content-Type':'application/json'
}


def get_ele(meter):
    """
    {
        'degree': {
            'remain': xxx,
            'before': xxx,
            'current': xxx
        },
        'ele': {
            'remain': xxx,
            'before': xxx,
            'current': xxx
        }
    }
    """
    ele_url = "http://202.114.38.46/SelectPage.aspx/SerBindTabDate"
    post_data = {
            "nodeInText": "%s*Meter" % meter,
            # "nodeInText": "3145*Meter",
            "PartList": "",
            "SelectPart": 1}
    r = requests.post(ele_url, data=json.dumps(post_data),
                      headers={'Content-Type': 'application/json'})
    content = r.content  # utf-8
    return content
