# coding: utf-8
"""
    lib.py
    ``````

    图书馆爬虫

    :MAINTAINER: neo1218
    :OWNER: muxistudio
"""

import re
import time
import base64
import requests
import datetime
from bs4 import BeautifulSoup
from . import lib_search_url, lib_me_url, lib_detail_url
from . import lib_renew_url, douban_url, headers
from . import proxy


def search_books(keyword):
    """
    :function: search_books
    :args:
        - keyword: 搜索关键字
    :rv:

    搜索图书结果

    :20161017:
        - 目前只能搜书名和部分作者
    """
    search_url = lib_search_url
    post_data = {
            'strSearchType': 'title', 'match_flag': 'forward',
            'historyCount': '1', 'strText': keyword, 'doctype': 'ALL',
            'displaypg': '100', 'showmode': 'list', 'sort': 'CATA_DATE',
            'orderby': 'desc', 'dept': 'ALL' }
    r = requests.get(search_url, post_data, headers=headers, proxies=proxy)
    soup = BeautifulSoup(r.content, 'lxml', from_encoding='utf-8')
    book_list_info = soup.find_all('li', class_='book_list_info')
    book_info_list = []
    for book_info in book_list_info:
        if book_info:
            book = book_info.find('a', href=re.compile('item.php*')).string
            marc_no_link = book_info.find('a').get('href')
            marc_no = marc_no_link.split('=')[-1]
            book_info_list.append({
                'book': book,
                'author': ' '.join(book_info.p.text.split()[2:-4]),
                'bid': 'fff',
                'intro': book_info.p.text.split()[-4],
                'id': marc_no
            })
    return book_info_list


def book_me(s):
    """
    :function: book_me
    :args:
        - s: 爬虫session对象
    :rv:

    我的图书馆爬虫
    """
    me_url = lib_me_url
    r = s.get(me_url, headers=headers)
    soup = BeautifulSoup(r.content, 'lxml', from_encoding='utf-8')
    bids = []
    a_tags = soup.find_all('a', class_="blue")
    for a_tag in a_tags:
        bids.append(a_tag.get('href').split("=")[-1])
    _my_book_list = soup.find_all('tr')[1:]
    my_book_list = []
    for index, _book in enumerate(_my_book_list):
        text = _book.text.split('\n')
        itime = text[3].strip(); otime = text[4].strip()
        date_itime = datetime.datetime.strptime(itime, "%Y-%m-%d")
        date_otime = datetime.datetime.strptime(otime, "%Y-%m-%d")
        ctime = datetime.datetime.now().strftime("%Y-%m-%d")
        dtime = time.mktime(date_otime.timetuple()) - \
                time.mktime(datetime.datetime.now().timetuple())

        renew_button = _book.find('input')['onclick']
        renew_info = [eval(i) for i in renew_button[renew_button.index('(')+1:\
                                       renew_button.index(')')].split(',')]
        bar_code = renew_info[0]
        check = renew_info[1]

        my_book_list.append({
            'book': text[2].split('/')[0].strip(),
            'author': text[2].split('/')[-1].strip(),
            'itime': str(itime),
            "otime": str(otime),
            "time": int(dtime/(24*60*60)),
            "room": text[6].strip(),
            "bar_code": bar_code,
            "check": check,
            "id": bids[index]
        })
    return my_book_list


def renew_book(s, bar_code, check):
    """
    :function: renew_book
    :args:
        - s: 爬虫session对象
    :rv:

    续借函数
    """
    renew_url = lib_renew_url
    now = int(time.time()*1000)
    payload = {
            'bar_code': bar_code,
            'check': check,
            'time': now
            }
    res = s.post(renew_url, params=payload)
    res_color = BeautifulSoup(res.content, "lxml", from_encoding='utf-8').find('font')['color']

    if res_color == 'green':
        res_code = 200
    else:
        res_string = BeautifulSoup(res.content, "lxml", from_encoding='utf-8').string.strip()
        early = u'\u4e0d\u5230\u7eed\u501f\u65f6\u95f4\uff0c\u4e0d\u5f97\u7eed\u501f\uff01'
        unavailable = u'\u8d85\u8fc7\u6700\u5927\u7eed\u501f\u6b21\u6570\uff0c\u4e0d\u5f97\u7eed\u501f\uff01'
        if res_string == early:
            res_code = 406
        elif res_string == unavailable:
            res_code = 403
        else:
            res_code = 400
    return res_code


def get_book(id):
    """
    :function: get_book
    :args:
        - id: 图书id

    图书详情
    """
    detail_url = lib_detail_url % id
    r = requests.get(detail_url, headers=headers, proxies=proxy)
    soup = BeautifulSoup(r.content, 'lxml', from_encoding='utf-8')

    # book = book; author = author
    book = str(soup.dd.a.string)
    author = str(soup.dd.text.split("/")[-1])
    isbn = ''.join(soup.find(
        'ul', class_="sharing_zy").li.a.get('href').split('/')[-2].split('-'))
    douban = douban_url % isbn
    rd = requests.get(douban, headers=headers)
    intro = rd.json().get('summary') or ""
    booklist = []
    _booklist = soup.find(id='tab_item').find_all('tr', class_="whitetext")
    for _book in _booklist:
        bid = _book.td.text
        tid = _book.td.next_sibling.next_sibling.string
        lit = _book.text.split()
        if '-' in lit[-1]:
            date = lit[-1][-10:]
            status = lit[-1][:2]
            booklist.append({
                "status": status, "room": lit[-2], "bid": bid,
                "tid": tid, "date": date })
        else:
            booklist.append({"status": lit[-1], "room": lit[-2], "tid": tid})
    return {
        'bid': bid, 'book': book,
        'author': author, 'intro': intro,
        'books': booklist
    }
