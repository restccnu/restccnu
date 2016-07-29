# coding: utf-8
#
import json
import requests
import HTMLParser
from bs4 import BeautifulSoup

html_parser = HTMLParser.HTMLParser()

headers = {
    'User-Agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:45.0) Gecko/20100101 Firefox/45.0",
    'Content-Type':'application/json'
}


def get_ele(meter, dor, typeit):
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
    # content = r.content  # utf-8
    content = r.json()
    main_html = content.get('d').split('|')[1].replace('', '')
    parse_html = html_parser.unescape(main_html)
    html = '<html><body>' + parse_html + '</body></html>'

    # return html
    soup = BeautifulSoup(html, 'lxml', from_encoding='utf-8')

    # degree_remain = soup.__str__()
    divMeterTopBox = soup.find('div', id='divMeterTopBox')
    divMeterTopBoxtrs = divMeterTopBox.tr.next_siblings

    _tr_dict = {}; _key = 0
    for tr in divMeterTopBoxtrs:
        _key += 1 
        _tr_dict.update({str(_key): tr}) 

    _ele = float(_tr_dict['4'].td.next_sibling.text[:-1])

    ele_remain = float(divMeterTopBox.find('td', id='tdSYValue').text[:-1])
    ele_before = _tr_dict['2'].td.next_sibling.text.split('：')[1][:-2]
    ele_current = _tr_dict['3'].td.next_sibling.text.split('：')[1][:-2]

    degree_remain = "%.2f" % (ele_remain / _ele)
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
        } }
