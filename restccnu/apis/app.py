# coding: utf-8
"""
    restccnu::apis::app
    ```````````````````

    华师匣子版本API

    :MAINTAINER: neo1218
    :OWNER: muxistudio
"""

import ast
from . import api
from restccnu import rds
from .decorators import tojson, admin_required
from flask import request, jsonify


@api.route('/app/', methods=['GET'])
@tojson
def get_app():
    """
    :function: get_app
    :args: none
    :rv: 所有版本列表

    redis1(6384): string
        key: "apps"
        value: "[{
            "name": "", "update": "", "version": "",
            "download": "", "intro": ""
        }]"

    获取华师匣子所有版本相关信息
    """
    if not rds.get('apps'):
        rds.set('apps', "[{'name':'ccnubox'}]")
        rds.save()
    apps = rds.get('apps')
    return ast.literal_eval(apps)


@api.route('/app/', methods=['POST'])
@admin_required
def new_app():
    """
    :function: new_app
    :args: none
    :rv: json message

    上传一个新的版本
    """
    if request.method == 'POST':
        name = request.get_json().get("name")
        version = request.get_json().get("version")
        download = request.get_json().get("download")
        update = request.get_json().get("update")
        intro = request.get_json().get("intro")
        size = request.get_json().get('size')
        app_data = {
                "name": name,
                "version": version,
                "download": download,
                "update": update,
                "intro": intro,
                "size": size,
        }
        if not rds.get('apps'):
            rds.set('apps', "[{'name':'ccnubox'}]")
        apps = ast.literal_eval(rds.get('apps'))
        apps.append(app_data)
        rds.set('apps', str(apps))
        rds.save()
        return jsonify({'msg': 'add new version data'}), 201


@api.route('/app/latest/', methods=['GET'])
@tojson
def get_latest_app():
    """
    :function: get_latest_app
    :args: none
    :rv: 返回最后一个版本列表(最新)

    获取最新版本华师匣子信息
    """
    if not rds.get('apps'):
        rds.set('apps', "[]")
    apps = rds.get("apps")
    return ast.literal_eval(apps)[-1]


@api.route('/app/<version>/', methods=['DELETE'])
@admin_required
def delete_version(version):
    """
    :function: delete_version
    :args: version
        - 待删除的版本号
    :rv: json message

    删除华师匣子特定版本version的信息
    """
    apps = ast.literal_eval(rds.get('apps'))
    for n, app in enumerate(apps):
        if app.get('version') == version:
            del apps[n]
    rds.set('apps', str(apps))
    rds.save()
    return jsonify({'msg': 'delete version %s' % version}), 200j
