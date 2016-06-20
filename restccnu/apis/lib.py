# coding: utf-8

import json
from . import api
from flask import request
from ..spiders.lib import search_books


@api.route('/lib/search/')
def api_search_books():
    keyword = request.args.get('keyword')
    if keyword:
        book_info_list = search_books(keyword)
        return json.dumps(book_info_list,
                          indent=1, ensure_ascii=False)
