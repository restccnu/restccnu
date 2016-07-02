# coding: utf-8
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
            "PartList": "",
            "SelectPart": 1}
    r = requests.post(ele_url, post_data, headers=headers)
    content = r.content
    return content
