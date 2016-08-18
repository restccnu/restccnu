# coding: utf-8

from . import api
from restccnu import rds
from .decorators import tojson


@api.route('/product/', methods=['GET'])
def get_products():
    """木犀应用展示"""
    pass


# PATCH: 更新时间戳(默认时间戳+1)
# DELETE: 删除特定的应用
# POST: 添加新的应用
