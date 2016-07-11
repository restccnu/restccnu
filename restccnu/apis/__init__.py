# coding: utf-8

from flask import Blueprint, jsonify


api = Blueprint('api', __name__)


@api.route('/')
def api_index():
    return jsonify({
        'meta': {
            'project': 'restccnu',
            'version': 'v1',
            'source code': 'https://github.com/Muxi-Studio/restccnu',
            'author': ['@neo1218', '@kasheemlew'],
        },
        'apis': {
            'Information Portal Login': '/api/info/login/',
            'library login': '/api/lib/login/',
            'book search': '/api/lib/search/?keyword=xxx&page=n',
            'book detail': '/api/lib/?id=xxxxxx&book=xxxx&author=xxxxx',
            'my library': '/api/lib/me/',
            'Class Schedule': '/api/table/?xnm=n&xqm=n',
        },
    }), 200


from . import login, lib, table, grades, ele
