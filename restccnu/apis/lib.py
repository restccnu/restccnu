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
    return get_book(id)


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


@api.route('/lib/renew/', methods=['POST'])
@require_lib_login
def api_renew_book(s, sid):
    """
    :function: api_renew_book
    :args:
        - s: 爬虫session对象
        - bar_code: 图书bar_code字段
        - check: 图书check字段
    """
    bar_code = request.get_json().get('bar_code')
    check = request.get_json().get('check')
    res_code = renew_book(s, bar_code, check)
    return jsonify({}), res_code


@api.route('/lib/create_atten/', methods=['POST'])
@require_lib_login
def api_create_atten(s, sid):
    """
    :function: api_create_atten
    :args:
        - s: 爬虫session对象
        - sid: 学号

    添加关注图书, 存储mongodb数据库
    """
    def init_atten(connection, book_name, book_id, book_bid, book_author, sid):
        """提醒初始化"""
        atten = connection.Attention()
        atten['bid'] = book_bid
        atten['book'] = book_name
        atten['id'] = book_id
        atten['author'] = book_author
        atten['sid'] = sid
        atten.save()
        return atten

    if request.method == 'POST':
        book_bid = request.get_json().get('bid')
        book_name = request.get_json().get('book')
        book_id = request.get_json().get('id')
        book_author = request.get_json().get('author')
        atten = connection.Attention.find_one({
            'bid': book_bid,
            'book': book_name,
            'id': book_id,
            'author': book_author,
            'sid': sid
        })
        if atten: return jsonify({}), 409

        atten = init_atten(connection, book_name, book_id, book_bid, book_author, sid)
        atten.save()
        return jsonify({}), 201


@api.route('/lib/get_atten/')
@require_lib_login
def api_get_atten(s, sid):
    """
    :function: api_get_atten
    :args:
        - s: 爬虫session对象
        - sid: 学号

    获取关注的图书列表
    """
    def isavailable(book_id, book_name, book_author):
        """获取图书是否可借"""
        book_list = get_book(book_id, book_name, book_author)
        for book in book_list['books']:
            if book['status'] == '\xe5\x8f\xaf\xe5\x80\x9f': return True
        return False

    all_list = list()
    available_list = list()

    attens = connection.Attention.find({'sid': sid})
    try: attens[0]
    except IndexError: return jsonify({}), 404

    for each_atten in attens:
        all_list.append({
            "bid": each_atten['bid'],
            "book": each_atten['book'],
            "id": each_atten['id'],
            "author": each_atten['author']
        })

    for each_in_all in all_list:
        if isavailable(each_in_all['id'], each_in_all['book'], each_in_all['author']):
            available_list.append({
                "bid": each_atten['bid'],
                "book": each_atten['book'],
                "id": each_atten['id'],
                "author": each_atten['author']
            })

    return jsonify({
        'all_list': all_list,
        'available_list': available_list
    }), 200


@api.route('/lib/del_atten/', methods=['DELETE'])
@require_lib_login
def api_del_atten(s, sid):
    """
    :function: api_del_atten
    :args:
        - s: 爬虫session对象
        - sid: 学号

    删除图书关注提醒
    """
    if request.method == 'DELETE':
        book_id = request.get_json().get('id')

        atten = connection.Attention.find_one({
            'id': book_id,
            'sid': sid,
        })

        if not atten: return jsonify({}), 404
        atten.delete()
        return jsonify({}), 200
