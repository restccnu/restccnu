# coding: utf-8
"""
    wsgi.py
    ```````

    wsgi入口模块, 用于服务器启动

    :MAINTAINER: neo1218
    :OWNER: muxistudio
"""

from gevent import monkey
monkey.patch_all()


from manage import app
