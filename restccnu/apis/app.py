# coding: utf-8

from . import api
from restccnu import rds
from .decorators import tojson, admin_required
from flask import request


@api.route('/app/', methods=['GET'])
@tojson
def get_app():
    """获取华师匣子所有版本相关信息"""
    if not rds.get('apps'):
        rds.set('apps', "[{'name':'ccnubox'}]")
        rds.save()
    apps = rds.get('apps')
    return eval(apps)


@api.route('/app/', methods=['POST'])
@tojson
@admin_required
def new_app():
    """上传一个新的版本"""
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
        apps = eval(rds.get('apps'))
        apps.append(app_data)
        rds.set('apps', str(apps))
        rds.save()
        return {'msg': 'add new version data'}, 201


@api.route('/app/latest/', methods=['GET'])
@tojson
def get_latest_app():
    """获取最新版本华师匣子信息"""
    if not rds.get('apps'):
        rds.set(apps, "[]")
    apps = rds.get("apps")
    return eval(apps)[-1]


@api.route('/app/<version>/', methods=['DELETE'])
@tojson
@admin_required
def delete_version(version):
    """删除华师匣子特定版本version的信息"""
    apps = eval(rds.get('apps'))
    for n, app in enumerate(apps):
        if app.get('version') == version:
            del apps[n]
    rds.set('apps', str(apps))
    rds.save()
    return {'msg': 'delete version %s' % version}, 200
