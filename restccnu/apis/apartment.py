# coding: utf-8

from restccnu.spiders.apartment import  _apartment_list
from . import api
from .decorators import tojson


@api.route('/apartment/')
@tojson
def api_get_apartment():
    return _apartment_list
