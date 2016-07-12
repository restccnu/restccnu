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
            'library': [
                {'library login': '/api/lib/login/'},
                {'book search': '/api/lib/search/?keyword=xxx&page=n'},
                {'book detail': '/api/lib/?id=xxxxxx&book=xxxx&author=xxxxx'},
                {'my library': '/api/lib/me/'},
            ],
            'Class Schedule': [
                {'class schedule query': '/api/table/?xnm=n&xqm=n'},
                {'add personal class': '/api/table/'},
                {'delete personal class': '/api/table/id/'}
            ],
        },
    }), 200


from . import login, lib, table, grades, ele
