# coding: utf-8

from .decorators import require_info_login, tojson
from . import api
from ..spiders.table import get_table
from ..spiders.login import info_login
from restccnu.errors import ForbiddenError


@api.route('/table/')
@tojson
@require_info_login
def api_get_table(s):
    rv = get_table(s)
    return str(rv)
