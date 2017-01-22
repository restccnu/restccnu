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
from restccnu.models import connection, Attention


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
def api_renew_book(s, bar_code, check):
    """
    :function: api_renew_book
    :args:
        - s: 爬虫session对象
        - bar_code: 图书bar_code字段
        - check: 图书check字段
    """
    res_code = renew_book(s, bar_code, check)
    return jsonify({}), res_code


@api.route('/lib/attention/', methods=['POST'])
@require_lib_login
def api_attention_book(s, sid):
    """
    :function: api_attention_book
    :args:
        - s: 爬虫session对象
        - sid: 学号

    添加关注图书, 存储mongodb数据库
    """
    if request.method == 'POST':
        user = connection.User.find_one({'sid': sid})
        if user is None:
            return jsonify({}), 403

        book_name = request.get_json().get('book_name')
        book = connection.Attention.find_one({'book_name': book_name})
        if book is None:
            atten = connection.Attention()
            atten['book_name'] = book_name
            atten['sid'] = [sid]
            atten.save()
        else:
            if sid in book['sid']:
                return jsonify({}), 409
            book['sid'].append(sid)

        return jsonify({}), 201


@api.route('/lib/haveattention/')
@require_lib_login
def api_haveattention(s, sid):
    """
    :function: api_haveattention
    :args:
        - s: 爬虫session对象
        - sid: 学号

    关注的图书已可借
    """
    def get_status(id):
        bs = get_book(id, '', '')['books']
        for b in bs:
            if b['status'] == '\xe5\x8f\xaf\xe5\x80\x9f':
                return 1
        return 0

    user = connection.User.find_one({'sid': sid})
    if user is None:
        return jsonify({}), 403

    books = []
    atten_list = []
    attens = connection.Attention.find()
    for atten in attens:
        if sid in atten['sid']:
            books.append(atten['book_name'])
    for book in books:
        book_list = search_books(book)
        ids = list(each['id'] for each in book_list)
        book = ''
        author = ''
        for id in ids:
            if get_status(id):
                atten_list.append(book)
                break

    if len(atten_list) == 0:
        return jsonify({}), 404
    else
        return jsonify({
            'book_list': book_list
            }), 200


@api.route('/lib/rmattention/', methods=['DELETE'])
@require_lib_login
def api_rmattention_book(s, sid):
    """
    :function: api_rmattention_book
    :args:
        - s: 爬虫session对象
        - sid: 学号

    删除关注图书
    """
    if request.method == 'DELETE':
        user = connection.User.find_one({'sid': sid})
        if user is None:
            return jsonify({}), 403

        book_name = request.get_json().get('book_name')
        book = connection.Attention.find_one({'book_name': book_name})
        if book is None:
            return jsonify({}), 404
        book['sid'].remove(sid)
        if len(book['sid']) == 0:
            book.delete()
        return jsonify({}), 201
