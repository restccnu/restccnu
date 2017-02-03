# coding: utf-8
"""
    ios_config.py
    ``````````````

    ios json config api

    :MAINTAINER: neo1218
    :OWNER: muxistudio
"""

import json
import ast
from restccnu import rds
from . import api
from .decorators import admin_required
from flask import request, jsonify


@api.route('/ios/config/', methods=['POST'])
@admin_required
def create_ios_config():
    """
    上传ios json配置
    """
    if request.method == 'POST':
        config = request.get_json().get('config')
        if not rds.get('ios_config'):
            rds.set('ios_config', config)
            rds.save()
            return jsonify({}), 201
        else: return jsonify({'msg': 'ios configuration already uploaded'})


@api.route('/ios/config/', methods=['GET'])
def get_ios_config():
    """
    获取ios json配置
    """
    if rds.get('ios_config'):
        config = rds.get('ios_config')
        return jsonify({
            'config': ast.literal_eval(config)
        }), 200
    else: return jsonify({}), 404


@api.route('/ios/config/', methods=['PUT'])
@admin_required
def update_ios_config():
    """
    更新ios json配置
    """
    if request.method == 'PUT':
        config = request.get_json().get('config')
        if rds.get('ios_config'):
            rds.set('ios_config', config)
            rds.save()
            return jsonify({}), 200
        else: return jsonify({}), 404
