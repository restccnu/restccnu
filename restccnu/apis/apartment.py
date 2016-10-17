# coding: utf-8
"""
    restccnu::apis::apartment
    `````````````````````````

    部门信息API

    :MAINTAINER: neo1218
    :OWNER: muxistudio

"""

from restccnu.spiders.apartment import  _apartment_list
from . import api
from .decorators import tojson


@api.route('/apartment/')
@tojson
def api_get_apartment():
    """
    :function api_get_apartment:
    :args: none
    :rv: 部门信息列表

    部门信息API
    """
    return _apartment_list
