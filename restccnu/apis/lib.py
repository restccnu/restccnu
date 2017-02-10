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
    def init_atten(connection):
        """提醒初始化"""
        atten = connection.Attention()
        atten['book_name'] = book_name
        atten['sid'] = list()
        atten.save()
        return atten

    if request.method == 'POST':
        user = connection.User.find_one({'sid': sid})
        if user is None:
            return jsonify({}), 403

        book_name = request.get_json().get('book_name')
        atten = connection.Attention.find_one({'book_name': book_name}) or init_atten(connection)

        if sid in atten['sid']:
            return jsonify({}), 409

        atten['sid'].append(sid)
        atten.save()
        return jsonify({}), 201


@api.route('/lib/haveattention/')
@require_lib_login
def api_have_attention(s, sid):
    """
    :function: api_have_attention
    :args:
        - s: 爬虫session对象
        - sid: 学号

    关注的图书可借提醒
    """
    def isavailable(keyword):
        """获取图书是否可借"""
        bs = search_books(keyword)
        for b in bs:
            book_list = get_book(b['id'], b['book'], b['author'])
            for book in book_list['books']:
                if book['status'] == '\xe5\x8f\xaf\xe5\x80\x9f':
                    return 1
        return 0

    user = connection.User.find_one({'sid': sid})
    if user is None:
        return jsonify({}), 403

    book_names = list()
    atten_list = list()
    attens = connection.Attention.find()

    # 获取关注的所有图书名字
    for atten in attens:
        if sid in atten['sid']:
            book_names.append(atten['book_name'])

    for book_name in book_names:
        if isavailable(book_name):
            atten_list.append(book_name)
            atten = connection.Attention.find_one({'book_name': book_name})
            atten['sid'].remove(sid)
            atten.save()
            if not len(atten['sid']): atten.delete()

    if not len(atten_list):
        return jsonify({}), 404
    else:
        return jsonify({'book_list': atten_list}), 200


@api.route('/lib/rmattention/', methods=['DELETE'])
@require_lib_login
def api_rmattention_book(s, sid):
    """
    :function: api_rmattention_book
    :args:
        - s: 爬虫session对象
        - sid: 学号

    删除图书关注提醒
    """
    if request.method == 'DELETE':
        book_name = request.get_json().get('book_name')

        user = connection.User.find_one({'sid': sid})
        if user is None:
            return jsonify({}), 403

        atten = connection.Attention.find_one({'book_name': book_name})
        if not atten: return jsonify({}), 404

        atten['sid'].remove(sid)
        atten.save()
        if not len(atten['sid']): atten.delete()
        return jsonify({}), 201
