# coding: utf-8
"""
    banners.py
    ``````````

    华师匣子bannerAPI

    :MAINTAINER: neo1218
    :OWNER: muxistudio
"""

import json
from . import api
from .. import rds, qiniu
from .decorators import admin_required
from flask import jsonify, request


# placeholder, make sure banners hash-list exist
rds.hset('banners', '_placeholder', '_placeholder')
rds.hset('banners_num', '_placeholder', '_placeholder')


@api.route('/banner/', methods=['GET'])
def get_banners():
    """
    :function: get_banners
    :args: none
    :rv: 按资源文件名排序的所有banner列表

    redis1(6384): hash list
        key: <banner name>-<qiniu resource name>
        value: <banner url>

    获取所有banner(列表, 按资源文件名排序)
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
                    "filename":  banner,
                    "num": rds.hget('banners_num', qiniu.url(banner))
                })
        # sorted_banners_list = sorted(banners_list, key=lambda x: x['filename'])
        sorted_banners_list = sorted(banners_list, key=lambda x: int(x['num']))
        return json.dumps(sorted_banners_list, indent=4, ensure_ascii=False), 200


@api.route('/banner/', methods=['POST'])
@admin_required
def new_banner():
    """
    :function: new_banner
    :args: none
    :rv: json message

    添加一个新的banner
    """
    if request.method == 'POST':
        img = request.get_json().get('img')
        url = request.get_json().get('url')
        num = request.get_json().get('num')

        # store in banners hash list
        rds.hset('banners', img, url)
        rds.hset('banners_num', qiniu.url(img), num)
        rds.save()

        return jsonify({}), 201


@api.route('/banner/', methods=['DELETE'])
@admin_required
def delete_banner():
    """
    :function: delete_banner
    :args: none
    :rv: json message

    根据名字删除banner, 删除排序表中的banner
    """
    if request.method == 'DELETE':
        # img = request.get_json().get('img')
        img = request.args.get('name')
        banners = rds.hgetall('banners')
        banners_num = rds.hgetall('banners_num')
        if img in banners:
            rds.hdel('banners', img)     # 删除banner
            rds.hdel('banners_num', img) # 删除排序表中的banner
            rds.save()
            return jsonify({}), 200
        else: return jsonify({}), 404


@api.route('/banner/', methods=['GET', 'PUT'])
@admin_required
def update_banner():
    """
    :function: update_banner
    
    更新banner(排序)
    """
    if request.method == 'PUT':
        img = request.get_json().get('img')  # 待修改的图片七牛外链
        num = request.get_json().get('num')  # 被修改后的排序num

        banners_num = rds.hgetall('banners_num')
        if img in banners_num:
            rds.hset('banners_num', img, num)
            rds.save()
            return jsonify({}), 200
        else: return jsonify({}), 404
