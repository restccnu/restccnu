# coding: utf-8
"""
    restccnu::apis
    ``````````````

    :MAINTAINER: neo1218
    :OWNER: muxistudio
"""

import os
from flask import Blueprint, jsonify, redirect


api = Blueprint('api',
     __name__,
     template_folder='templates'
)


@api.route('/')
def api_index():
    return jsonify({
        'meta': {
            'project': 'restccnu',
            'version': 'v1.0.3',
            'source code': 'https://github.com/Muxi-Studio/restccnu',
            'lang': 'python',
            'author': ['@neo1218', '@kasheemlew'],
            'status': '✅',
            'proxy': os.getenv('PROXY')
        },
    }), 200


from . import login, lib, table, grades, ele, board, banners, apartment, app, \
              patch, product, calendars, start, website, classroom
# ios 
from . import ios_banners, ios_calendars, push, ios_feedback, ios_config
