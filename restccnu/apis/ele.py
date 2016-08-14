# coding: utf-8

from . import api
from flask import jsonify, request
from restccnu.models import connection
from ..spiders.meter_index import colour_meter_index
from ..spiders.ele import get_ele
from .decorators import tojson


@api.route('/ele/', methods=['POST'])
@tojson
def api_get_ele():
    dor_obj = connection.Dormitory.find_one()
    dor_dict = dor_obj.get('meter')

    if request.method == 'POST':
        dor = request.get_json().get('dor')
        typeit = request.get_json().get('type')
        _dor = dor_dict.get(dor)
        if _dor is None:
            return {}, 202
        if typeit == 'light':
            meter = _dor[0]
        elif typeit == 'air':
            meter = _dor[1]
        rv = get_ele(meter, dor, typeit)
        return rv  # return data


@api.route('/store_ele/', methods=['POST'])
@tojson
def api_store_ele():
    if request.method == 'POST':
        if connection.Dormitory.find_one().get('meter') is None or \
            len(connection.Dormitory.find_one().get('meter').keys()) < 2:
            _meter_index = colour_meter_index()
            dormitory = connection.Dormitory.find_one()
            dormitory['meter'] = _meter_index
            dormitory.save()
            return {'msg': "dormitory info stored",
                    'dor_dict': connection.Dormitory.find_one().get('meter')}
        else:
            return {'msg': "dormitory info already stored"}


@api.route('/flush_ele/', methods=['DELETE'])
@tojson
def api_flush_ele():
    if request.method == 'DELETE':
        if len(connection.Dormitory.find_one().get('meter').keys()) > 1:
            dormitory = connection.Dormitory.find_one()
            dormitory['meter'] = {'_meter': []}
            dormitory.save()
            return {'msg': "flush dormitory info",
                    'dor_dict': connection.Dormitory.find_one().get('meter')}
        else:
            return {'msg': "dormitory info is None"}


@api.route('/ele_dict/', methods=['GET'])
@tojson
def api_get_eledict():
    dor_dict = connection.Dormitory.find_one().get('meter')
    return {'dor_dict': dor_dict}
