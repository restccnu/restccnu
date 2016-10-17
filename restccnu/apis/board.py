# -*- coding: utf-8 -*-
"""
    board.py
    ````````

    通知公告API
    
    :MAINTAINER: kasheelew
    :OWNER: muxistudio
"""

import json
from . import api
from .. import board
from flask import request, jsonify
from ..spiders.board import get_all_board
from .decorators import tojson


@api.route('/info/')
def get_info():
    """
    :function: get_info
    :args: none
    :rv: all board list

    返回所有通知公告(3个平台每个平台5个)
    """
    if not board.get('board_list'):
        board_list = get_all_board()
        board.set('board_list', board_list)
    all_board = eval(board.get('board_list'))
    return jsonify(all_board)
