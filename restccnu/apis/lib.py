# coding: utf-8
"""
    lib.py
    ``````

    图书馆API模块

    :MAINTAINER: neo1218
    :OWNER: muxistudio
"""

import json
from . import api
from flask import request, jsonify
from ..spiders.lib import search_books, get_book, book_me, renew_book
from .decorators import tojson, require_lib_login
from .paginate import _Pagination


@api.route('/lib/search/')
@tojson
def api_search_books():
    """
    :function: api_search_books
    :args: none
    :rv: 图书信息

    搜索图书, 返回图书相关信息, 分页(每页20条)
    """
    per_page = 20
    keyword = request.args.get('keyword')
    page = int(request.args.get('page') or '1')
    if keyword:
        book_info_list = search_books(keyword)
        pg_book_info_list = _Pagination(book_info_list, page, per_page)
        return {'meta': {
                'max': pg_book_info_list.max_page,
                'per_page': per_page },
            'results': book_info_list[(page-1)*per_page:page*per_page]}


@api.route('/lib/')
@tojson
def api_book_detail():
    """
    :function: api_book_detail
    :args: none
    :rv: 图书详细信息

    图书详情
    """
    id = request.args.get('id')
    book = request.args.get('book')
    author = request.args.get('author')
    return get_book(id, book, author)


@api.route('/lib/me/')
@require_lib_login
@tojson
def api_book_me(s, sid):
    """
    :function: api_book_me
    :args:
        - s: 爬虫session对象
        - sid: 学号
    """
    return book_me(s)


@api.route('/lib/renew/')
@require_lib_login
@to_json
def api_renew_book(s, bar_code, check):
    """
    :function: api_renew_book
    :args:
        - s: 爬虫session对象
        - bar_code: 图书bar_code字段
        - check: 图书check字段
    """
    return renew_book(s, bar_code, check)
