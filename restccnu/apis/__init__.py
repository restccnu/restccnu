# coding: utf-8
"""
    restccnu::apis
    ``````````````

    :MAINTAINER: neo1218
    :OWNER: muxistudio
"""

from flask import Blueprint, jsonify, redirect


api = Blueprint('api', __name__)


@api.route('/')
def api_index():
    return jsonify({
        'meta': {
            'project': 'restccnu',
            'version': 'v1',
            'source code': 'https://github.com/Muxi-Studio/restccnu',
            'lang': 'python',
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
            'Grade Query': {
                'query': '/api/grade/search/?xnm=n&xqm=n',
                'detail query': '/api/grade/detail/search/?xnm=x&xqm=x&course=x&jxb_id=x'
            },
            'Info API': '/api/info/',
            'Electric bill API': '/api/ele/',
            'Apartment info API': '/api/apartment/',
            'Static Management': [
                {'banner api': '/api/banner/'},
                {'calendar api': '/api/calendar'},
                {'start api': '/api/start/'}
            ],
            'Version Management': {
                'app version management': [
                    {'all ccnubox version': '/api/app/'},
                    {'add a new version': '/api/app/'},
                    {'delete a specific version': '/api/app/'},
                    {'ccnubox latest version': '/api/app/latest/'}
                ],
                'patch version management': [
                    {'all ccnubox patches version': '/api/patch/'},
                    {'add a new patch version': '/api/patch/'},
                    {'delete a specific patch version': '/api/patch/'},
                    {'latest ccnubox patch version': '/api/patch/latest/'}
                ],
            },
            'muxistudio products': [
                {'muxistudio products': '/api/product/'},
                {'add a product': '/api/product/'},
                {'delete a product': '/api/product/'},
                {'update a product': '/api/product/'},
            ],
        },
    }), 200


from . import login, lib, table, grades, ele, board, banners, apartment, app, \
              patch, product, calendars, start
