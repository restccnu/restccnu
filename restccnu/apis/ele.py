# coding: utf-8
"""
    ele.py
    ``````

    电费查询

    :MAINTAINER: neo1218
    :OWNER: muxistudio
"""

from . import api
from flask import jsonify, request
from restccnu.models import connection
from ..spiders.meter_index import colour_meter_index
from ..spiders.ele import get_ele
from .decorators import tojson, admin_required


@api.route('/ele/', methods=['POST'])
@tojson
def api_get_ele():
    """
    :function: api_get_ele
    :args: none
    :rv: get_ele spider function return value

    电费查询(light, air)
    """
    dor_obj = connection.Dormitory.find_one()
    dor_dict = dor_obj.get('meter')

    if request.method == 'POST':
        dor = request.get_json().get('dor')
        typeit = request.get_json().get('type')
        _dor = dor_dict.get(dor)
        if _dor is None:
            return {}, 404
        if typeit == 'light':
            meter = _dor[0]
        elif typeit == 'air':
            if len(_dor) == 1:
                meter = 0
            else: meter = _dor[1]
        rv = get_ele(meter, dor, typeit)
        return rv  # return data


@api.route('/store_ele/', methods=['POST'])
@tojson
@admin_required
def api_store_ele():
    """
    :function: api_store_ele
    :args: none
    :rv: json message

    更新mongodb数据库宿舍电表存储
    """
    if request.method == 'POST':
        mongobj = connection.Dormitory.find_one()
        if len(mongobj.get('meter').get('_meter')) == 0:
            _meter_index = colour_meter_index()  # get dor_meter list
            mongobj['meter'] = _meter_index
            mongobj.save()
            return {'msg': "dormitory info stored",
                    'dor_dict': mongobj.get('meter')}
        else:
            return {'msg': "dormitory info already stored"}


@api.route('/flush_ele/', methods=['DELETE'])
@tojson
@admin_required
def api_flush_ele():
    """
    :function: api_flush_ele
    :args: none
    :rv: json message

    清除当前mongodb数据库宿舍电表存储
    """
    if request.method == 'DELETE':
        mongobj = connection.Dormitory.find_one()
        if len(mongobj.get('meter').keys()) > 1:
            mongobj['meter'] = {'_meter': []}  #'meter' is required,placeholder
            mongobj.save()
            return {'msg': "flush dormitory info",
                    'dor_dict': mongobj.get('meter')}
        else:
            return {'msg': "dormitory info is None"}


@api.route('/ele_dict/', methods=['GET'])
@admin_required
def api_get_eledict():
    """
    :function: api_get_eledict
    :args: none
    :rv: dormitory electron dict

    返回mongodb存储的寝室电表字典
    """
    dor_dict = connection.Dormitory.find_one().get('meter')
    return jsonify({
            'sum': len(dor_dict.keys()),
            'dor_dict': dor_dict
    })
