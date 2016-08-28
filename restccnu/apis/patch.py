# coding: utf-8

from . import api
from restccnu import rds
from .decorators import tojson, admin_required
from flask import request, jsonify


@api.route('/patch/', methods=['GET'])
@tojson
def get_patch():
    """获取华师匣子所有补丁包相关信息"""
    if not rds.get('patches'):
        rds.set('patches', "[{'name':'ccnubox_patch'}]")
        rds.save()
    patches = rds.get('patches')
    return eval(patches)


@api.route('/patch/', methods=['POST'])
@admin_required
def new_patch():
    """上传一个新的补丁包"""
    if request.method == 'POST':
        version = request.get_json().get("version")
        download = request.get_json().get("download")
        update = request.get_json().get("update")
        intro = request.get_json().get("intro")
        size = request.get_json().get('size')
        patch_data = {
                "version": version,
                "download": download,
                "update": update,
                "intro": intro,
                "size": size,
        }
        if not rds.get('patches'):
            rds.set('patches', "[{'name':'ccnubox_patch'}]")
        patches = eval(rds.get('patches'))
        patches.append(patch_data)
        rds.set('patches', str(patches))
        rds.save()
        return jsonify({'msg': 'add new patch version'}), 201


@api.route('/patch/latest/', methods=['GET'])
@tojson
def get_latest_patch():
    """获取最新版本华师匣子补丁信息"""
    if not rds.get('patches'):
        rds.set(patches, "[]")
    patches = rds.get("patches")
    return eval(patches)[-1]


@api.route('/patch/<version>/', methods=['DELETE'])
@admin_required
def delete_patch_version(version):
    """删除华师匣子特定版本补丁的信息"""
    patches = eval(rds.get('patches'))  # eval is evil
    for n, patch in enumerate(patches):
        if patch.get('version') == version:
            del patches[n]
    rds.set('patches', str(patches))
    rds.save()
    return jsonify({'msg': 'delete patch version %s' % version}), 200