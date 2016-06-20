# coding: utf-8

import json
from . import api
from flask import request
from ..spiders.lib import search_books
from .decorators import tojson


@api.route('/lib/search/')
@tojson
def api_search_books():
    keyword = request.args.get('keyword')
    if keyword:
        book_info_list = search_books(keyword)
        return book_info_list, 200
