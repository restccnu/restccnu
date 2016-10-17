# coding: utf-8
"""
    product.py
    ``````````

    木犀产品展示API

    :MAINTAINER: neo1218
    :OWNER: muxistudio
"""

from . import api
from restccnu import rds  # 应用信息存入6384redis中
from .decorators import tojson
from flask import jsonify, request
from .decorators import admin_required
import time


@api.route('/product/', methods=['GET'])
def get_product():
    """
    :function: get_product

    redis1(6384)~products
        key: products
        value: "{ 'update': 时间戳,
            '_products': [{
                'name': name, 'url': url
                'icon': icon, 'intro': intro
            }]
        }"

    木犀应用展示
    """
    if eval(rds.get('products') or '{}'):
    	products_dict = eval(rds.get('products'))
    	return jsonify(products_dict)
    else: return jsonify({})


@api.route('/product/', methods=['PUT'])
@admin_required
def add_product():
    """
    :function: add_product

    添加一个木犀的产品
    """
    if request.method == 'PUT':
        name = request.get_json().get('name')
        icon = request.get_json().get('icon')
        url  = request.get_json().get('url')
        intro = request.get_json().get('intro')

        products_dict = eval(rds.get('products') or '{"_products":[], "update":""}')
        products_list = products_dict.get('_products')
        products_list.append({
	    'name': name, 'icon': icon, 'url': url, 'intro': intro
	})
        products_dict['_products'] = products_list
        products_dict['update'] = time.time()

	rds.set('products', products_dict)
	rds.save()
	return jsonify({}), 200


@api.route('/product/', methods=['DELETE'])
@admin_required
def delete_product():
    """
    :function: delete_product

    删除某个应用
    """
    if request.method == 'DELETE':
        if request.args.get('name'):
            name = request.args.get('name')
            products_dict = eval(rds.get('products') or '{"_products":[], "update":""}')
            products_list = products_dict.get('_products')
            if products_list:
                for product in products_list:
                    if product.get('name') == name:
                        products_list.remove(product)
                        products_dict['_products'] = products_list
                        products_dict['update'] = time.time()
                        rds.set('products', products_dict)
                        rds.save()
                        return jsonify({}), 200
            return jsonify({}), 404
