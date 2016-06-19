# coding: utf-8

from . import api
from .authentication import info_login
from .errors import ForbiddenError
from flask import jsonify
import json


@api.route('/table/')
def mock_get_table():
    try:
        s = info_login()
    except ForbiddenError as e:
        return jsonify({}), e.status_code
    else:
        return json.dumps([
            {
                "id": "1",
                "course": "安卓开发",
                "teacher": "逍遥",
                "weeks": "1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19",
                "day": 1,
                "start": 1,
                "during": 2,
                "place": "9-21"
            },
            {
                "id": "2",
                "course": "Python开发",
                "teacher": "朱承浩",
                "weeks": "2, 4, 6, 8, 10, 12, 14, 16, 18",
                "day": 3,
                "start": 3,
                "during": 4,
                "place": "8202"
            }
        ], indent=1, ensure_ascii=False)
