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
    if not connection.Dormitory.find_one():
        # 现实爬取
        _meter_index = colour_meter_index()
        dormitory = connection.Dormitory()
        dormitory['meter'] = _meter_index
        dormitory.save()
    dor_obj = connection.Dormitory.find_one()
    dor_dict = dor_obj.get('meter')

    if request.method == 'POST':
        dor = request.get_json().get('dor')
        typeit = request.get_json().get('type')
        _dor = dor_dict.get(dor)
        if typeit == 'light':
            meter = _dor[0]
        elif typeit == 'air':
            meter = _dor[1]
        rv = get_ele(meter, dor, typeit)
        return rv  # return data
