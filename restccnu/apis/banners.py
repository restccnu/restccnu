# coding: utf-8

"""
    banners.py
    ``````````

    ccnubox banner crud
"""

import json
from . import api
from .. import rds, qiniu
from .decorators import admin_required
from flask import jsonify, request


# placeholder, make sure banners hash-list exist
rds.hset('banners', '_placeholder', '_placeholder')


@api.route('/banner/', methods=['GET'])
def get_banners():
    """
    get all banners(a hash list)
    [{'filename':'url'}, {'filename':'url'}]
    """
    if rds.hlen('banners') == 1:
        return jsonify({}), 404
    else:
        banners_list = []
        banners = rds.hgetall('banners')
        for banner in banners:
            if banner != '_placeholder':
                try:
                    update = qiniu.info(banner)['putTime']
                except KeyError:
                    update = qiniu.info(banner)
                banners_list.append({
                    "img": qiniu.url(banner),
                    "url": banners.get(banner),
                    "update": update,
                })
        return json.dumps(banners_list, indent=4, ensure_ascii=False), 200


@api.route('/banner/', methods=['POST'])
@admin_required
def new_banner():
    """
    add a new banner
    """
    if request.method == 'POST':
        img = request.get_json().get('img')
        url = request.get_json().get('url')

        # store in banners hash list
        rds.hset('banners', img, url)
        rds.bgsave()

        return jsonify({}), 201


@api.route('/banner/', methods=['DELETE'])
@admin_required
def delete_banner():
    """
    delete a banner by name...
    """
    if request.method == 'DELETE':
        img = request.get_json().get('img')
        banners = rds.hgetall('banners')
        if img in banners:
            rds.hdel('banners', img)
            rds.bgsave()
            return jsonify({}), 200
        else: return jsonify({}), 404
