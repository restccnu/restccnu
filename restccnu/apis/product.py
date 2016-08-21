# coding: utf-8

from . import api
from restccnu import rds  # 应用信息存入6384redis中
from .decorators import tojson


@api.route('/product/', methods=['GET'])
def get_products():
    """木犀应用展示"""
    pass