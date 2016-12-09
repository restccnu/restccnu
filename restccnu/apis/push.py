# coding: utf-8
"""
    push.py
    ```````

    ios notification push api

    :MAINTAINER: neo1218
    :OWNER: muxistudio
"""

import os
import ast
from pushjack import APNSClient
# from pushjack import APNSSandboxClient
from flask import request, jsonify
from restccnu import rds
from .decorators import admin_required
from . import api


@api.route('/push/register/', methods=['GET', 'POST'])
@admin_required
def push_register():
    """
    :function: push_register
    :args: none
    :rv: success message

    redis(6384): string
        key: "ids"
        vlaue: "['id1', 'id2']"

    注册ios设备的unique_id
    """
    if request.method == 'POST':
        unique_id = request.get_json().get('unique_id')
        sid = request.get_json().get('sid')  # 学号
        # 将unique_id写入数据库
        if not rds.get('ids'):
            rds.set('ids', "[]")
            rds.save()
        ids = ast.literal_eval(rds.get('ids'))
        if unique_id not in ids:
            if not sid:
                ids.append(unique_id)
            else: ids.append("%s:%s" % (unique_id, sid))
        elif unique_id in ids:
            index = ids.index(unique_id)
            del ids[index]
            ids.append("%s:%s" % (unique_id, sid))
        # db commit
        rds.set('ids', ids)
        rds.save()
            
        return jsonify({
            'message': 'add new unique_id'
        }), 201


@api.route('/push/ids/', methods=["GET"])
@admin_required
def get_ids():
    """
    :function: get_ids
    :args: 无
    :rv: 所有设备id json列表

    返回所有注册的设备id
    """
    return jsonify({
        'ids': ast.literal_eval(rds.get('ids'))
    })


@api.route('/push/', methods=['GET', 'POST'])
@admin_required
def push_notification():
    """
    :function: push_notification
    :args: 无
    :rv: 无, 如果出错, 返回错误设备token和信息
    """
    if request.method == 'POST':
        title = request.get_json().get('title')
        userinfo = request.get_json().get('userinfo')
        
        _ids = []
        ids = ast.literal_eval(rds.get('ids'))
        for id in ids:
            _ids.append(id.split(':')[0])

        client = APNSClient(
        # client = APNSSandboxClient(
            certificate=os.getenv("IOS_CERTIFICATE"),
            default_error_timeout=10,
            default_expiration_offset=2592000,
            default_batch_size=100
        )

        res = client.send(_ids, title,
                          extra=userinfo)
        return jsonify({
            "error": str(res.token_errors)
        })
