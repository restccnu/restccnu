# coding: utf-8

import os
from .. import app, board, make_celery
from ..spiders.board import get_all_board


celery = make_celery(app)


@celery.task(name='cute_board_spider')
def cute_board_spider():
    board.flushdb()
    board_list = get_all_board()
    board.save('board_list', board_list)
    board.save()
