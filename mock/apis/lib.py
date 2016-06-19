# coding: utf-8

from . import api
from flask import url_for, jsonify
from .authentication import lib_login
from .errors import ForbiddenError
import json


@api.route('/lib/search/')
def mock_lib_search():
    return jsonify({
        "meta": {
            "next": "",
            "last": url_for('api.mock_lib_search',
                            page=1, keywords='安卓', _external=True),
            "per_page": 1
        },
        "results": [
            {
                "book": "安卓开发从入门到放弃",
                "author": "超哥",
                "bid":  "TP311.12/QZY",
                "intro": "安卓史上最强图书",
                "id": "VFAzMTEuMTIvUVpZ"
            }
        ]
    })


@api.route('/lib/<int:id>/')
def mock_lib_id(id):
    return jsonify({
        "bid": "TP311.12/QZY",
        "book": "安卓开发从入门到放弃",
        "author": "超哥",
        "intro": "安卓史上最强图书, 安卓开发入门经典, 大神必备, 人手一份!",
        "books": [
            {
                "status": "可借",
                "room": "借书处—计算机科学学院资料室",
            },
            {
                "status": "不可借",
                "room": "图书馆",
                "date": "2016-08-15"
            }
        ]
    })


@api.route('/lib/me/')
def mock_lib_me():
    try:
        s = lib_login()
    except ForbiddenError as e:
        return jsonify({}), e.status_code
    else:
        return json.dumps([
            {
                "book": '安卓开发从入门到放弃',
                "author": '超哥',
                "itime": '2016-06-19',
                "otime": '2016-06-29',
                "time": '10'
            },
            {
                "book": 'Python从放弃到自缢',
                "author": '朱承浩',
                "itime": '2016-06-19',
                "otime": '2016-06-29',
                "time": '10'
            }
        ], indent=1, ensure_ascii=False)
