# -*- coding: utf-8 -*-

import json
from . import api
from flask import request, jsonify
from ..spiders.board import get_all_board
from .decorators import tojson


@api.route('/api/info/')
@tojson
def all_board():
    all_board = get_all_board()
    return all_board
