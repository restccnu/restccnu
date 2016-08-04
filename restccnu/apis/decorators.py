# coding: utf-8

import os
import base64
import functools
import json
from flask import make_response, jsonify, request, abort
from restccnu.spiders.login import info_login, lib_login
from restccnu.errors import ForbiddenError


def tojson(f):
    @functools.wraps(f)
    def decorator(*args, **kwargs):
        rv = f(*args, **kwargs)
        status_or_headers = None
        headers = None
        if isinstance(rv, tuple):
            rv, status_or_headers, headers = rv + (None, ) * (3 - len(rv))
        if isinstance(status_or_headers, (dict, list)):
            headers, status_or_headers = status_or_headers, None

        rv = json.dumps(rv, indent=1, ensure_ascii=False)
        rv = make_response(rv)
        if status_or_headers is not None:
            rv.status_code = status_or_headers
        if headers is not None:
            rv.headers.extend(headers)
        return rv
    return decorator


def require_info_login(f):
    @functools.wraps(f)
    def decorator(*args, **kwargs):
        try:
            s, sid = info_login()
        except ForbiddenError as e:
            return jsonify({}), e.status_code
        else:
            rv = f(s, sid, *args, **kwargs)
            return rv
    return decorator


def require_lib_login(f):
    @functools.wraps(f)
    def decorator(*args, **kwargs):
        try:
            s, sid = lib_login()
        except ForbiddenError as e:
            return jsonify({}), e.status_code
        else:
            rv = f(s, sid, *args, **kwargs)
            return rv
    return decorator


def admin_required(f):
    @functools.wraps(f)
    def decorator(*args, **kwargs):
        # http basic auth: Basic base64(email:password)
        token_header = request.headers.get('authorization', None)
        if token_header:
            email_pass = base64.b64decode(token_header[6:])
            email = email_pass.split(':')[0]
            password = email_pass.split(':')[1]
            if email == os.getenv('QINIU_EMAIL') and \
               password == os.getenv('QINIU_PASS'):
                return f(*args, **kwargs)
            else:
                return jsonify({'msg': 'unauthorized'}), 401
        else:
            return jsonify({'msg': 'forbidden'}), 403
    return decorator
