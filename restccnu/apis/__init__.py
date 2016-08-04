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
            'Library': [
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
            'Grade Query': '/api/grade/search/?xnm=n&xqm=n',
            'Info API': '/api/info/',
            'Electric bill API': '/api/ele/',
            'Apartment info API': '/api/apartment/',
            'Static Management': [
                {'banner api': '/api/banner/'},
                {'calendar api': '/api/calendar'}
            ],
            'App Version Management': [
                {'all ccnubox version': '/api/app/'},
                {'add a new version': '/api/app/'},
                {'delete a specific version': '/api/app/'},
                {'ccnubox latest version': '/api/app/latest/'}
            ],
        },
    }), 200


from . import login, lib, table, grades, ele, board, static, apartment, app
