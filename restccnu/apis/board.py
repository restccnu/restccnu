# -*- coding: utf-8 -*-

import json
from . import api
from .. import board
from flask import request, jsonify
from ..spiders.board import get_all_board
from .decorators import tojson


@api.route('/info/')
def get_info():
    if not board.get('board_list'):
        board_list = get_all_board()
        board.set('board_list', board_list)
    all_board = eval(board.get('board_list'))
    return jsonify(all_board)
