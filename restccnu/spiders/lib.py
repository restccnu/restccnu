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
            bid_lit = book_info.h3.text.split()
            try:
                int(bid_lit[-1])
            except ValueError as e:
                bid = bid_lit[-1]
            else:
                bid = ' '.join(bid_lit[-2:])
            book = book_info.find('a', href=re.compile('item.php*')).string
            marc_no_link = book_info.find('a').get('href')
            marc_no = marc_no_link.split('=')[-1]
            book_info_list.append({
                'book': book,
                'author': ' '.join(book_info.p.text.split()[2:-4]),
                'bid': bid,
                'intro': 'intro',  # no intro ?
                'id': marc_no
            })
    return book_info_list


# http://202.114.34.15/opac/item.php?marc_no=0001364670
def get_book():
    pass
