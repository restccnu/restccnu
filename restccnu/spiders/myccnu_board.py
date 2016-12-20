# -*- coding: utf-8 -*-
"""
    myccnu_board.py
    ````````

    掌上华师公告

    :MAINTAINER: kasheemlew
    :OWNER: muxistudio

"""
import requests
import sys
from bs4 import BeautifulSoup
from . import myccnu_url
from . import myccnu_cookie
from .. import board

reload(sys)
sys.setdefaultencoding('utf-8')

def get_myccnu_board():
    headers = {'Cookie': myccnu_cookie}
    payload = {
            's': '/addon/CcnuNotification/CcnuNotification/tongzhi.html',
            'token': 'gh_826f52e085d9'
            }
    r = requests.get(
            '/'.join([myccnu_url, 'index.php']),
            params = payload,
            headers = headers
            )
    board_content = r.content
    board_soup = BeautifulSoup(board_content, 'lxml')
    board_ul = board_soup.find('ul', class_='collection')
    board_lis = board_ul.find_all('li')

    result_list = []
    for li in board_lis:
        tag = li.find('i', class_='material-icons circle').string.strip()
        title = li.find('strong').string.strip()
        summary = li.find('p').string.strip()
        second_page = ''.join([myccnu_url, li.find('p').find_next_sibling().find('a')['href']])
        result_list.append({
            'tag': tag,
            'title': title,
            'summary': summary,
            'second_page': second_page,
            })

    return result_list
