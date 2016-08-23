# coding: utf-8

import os
from .. import app, board, make_celery
from ..spiders.board import get_all_board
from werkzeug.exceptions import InternalServerError


celery = make_celery(app)


@celery.task(name='cute_board_spider')
def cute_board_spider():
    try:
        board_list = get_all_board()
    except:
        raise InternalServerError()
    board.flushdb()
    board.set('board_list', board_list)
    board.save()
