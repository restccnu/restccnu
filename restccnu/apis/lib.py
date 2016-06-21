# coding: utf-8

import json
from . import api
from flask import request, jsonify
from ..spiders.lib import search_books
from .decorators import tojson
from .paginate import _Pagination


@api.route('/lib/search/')
@tojson
def api_search_books():
    per_page = 5
    keyword = request.args.get('keyword')
    page = int(request.args.get('page') or '1')
    if keyword:
        book_info_list = search_books(keyword)
        pg_book_info_list = _Pagination(book_info_list, page, per_page)
    return {'meta': {
                'next': pg_book_info_list.next_page,
                'last': pg_book_info_list.last_page,
                'per_page': per_page },
            'results': book_info_list[(page-1)*per_page:page*per_page]}
