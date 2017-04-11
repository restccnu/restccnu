# -*- coding: utf-8 -*-
"""
    board.py
    ````````

    通知公告API

    :MAINTAINER: kasheemlew
    :OWNER: muxistudio
"""

import ast
import json
from . import api
from .. import board, webview_board
from flask import request, jsonify
from ..spiders.board import get_all_board, get_webview_board
from .decorators import tojson


@api.route('/info/')
def api_get_info():
    """
    :function: get_info
    :args: none
    :rv: all board list

    返回所有通知公告(3个平台每个平台5个)
    """
    if not board.get('board_list'):
        board_list = get_all_board()
        board.set('board_list', board_list)
    all_board = ast.literal_eval(board.get('board_list'))
    return jsonify(all_board)


@api.route('/webview_info/')
def api_webview_info():
    """
    :function: webview_info
    :args: none
    :rv: all board with format

    返回带有格式的通知公告(3个平台每个平台5个)
    """
    webview_board_list = webview_board.get('webview_board_list')
    if not webview_board_list:
        board_list = get_webview_board()
        webview_board.set('webview_board_list', board_list)
    all_board = ast.literal_eval(webview_board.get('webview_board_list'))
    return jsonify(all_board)
