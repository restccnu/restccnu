# coding: utf-8

import re
import requests
from bs4 import BeautifulSoup
import base64


def search_books(keyword):
    search_url = "http://202.114.34.15/opac/openlink.php"
    post_data = {
            'strSearchType': 'title',
            'match_flag': 'forward',
            'historyCount': '1',
            'strText': keyword,
            'doctype': 'ALL',
            'displaypg': '100',  # tomorrow
            'showmode': 'list',
            'sort': 'CATA_DATE',
            'orderby': 'desc',
            'dept': 'ALL'
    }
    r = requests.get(search_url, post_data)
    # r.encoding = 'utf-8'
    # soup = BeautifulSoup(r.content, 'lxml', from_encoding='iso-8859-1')
    soup = BeautifulSoup(r.content, 'lxml', from_encoding='utf-8')
    book_list_info = soup.find_all('li', class_='book_list_info')
    book_info_list = []
    for book_info in book_list_info:
        if book_info:
            bid = book_info.h3.text.split()[-1]
            book = book_info.h3.text.split()[0]
            book_info_list.append({
                'book': book,
                'author': book_info.p.text.split()[3],
                'bid': bid,
                'intro': 'intro',  # no intro ?
                'id': base64.b64encode(bid)
            })
    return book_info_list
    # return book_list_info[0]
