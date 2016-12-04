#coding: utf-8
"""
    restccnu::apis::website

    常用网站API

    :MAINTAINER: neo1218
    :OWNER: muxistudio

"""

from restccnu.spiders.website import _site_list
from . import api
from .decorators import tojson


@api.route('/site/')
@tojson
def apt_get_site():
    """
    :function api_get_site:
    :args: none
    :rv: 常用网站列表

    常用网站API
    """
    return _site_list
