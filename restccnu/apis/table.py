# coding: utf-8

from flask import request
from .decorators import require_info_login, tojson
from . import api
from ..spiders.table import get_table
from ..spiders.login import info_login
from restccnu.errors import ForbiddenError


@api.route('/table/')
@tojson
@require_info_login
def api_get_table(s):
    xnm = request.args.get('xnm')
    xqm = request.args.get('xqm')
    sid = request.args.get('sid')
    rv = get_table(s, sid, xnm, xqm)
    return rv
