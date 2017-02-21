# coding: utf-8
"""
    restccnu
    ````````

    华师匣子API

    :MAINTAINER: neo1218
    :OWNER: muxistudio
"""

import os
import redis
from flask import Flask, render_template, request
from flask_zero import Qiniu
from flask_mail import Mail
from celery import Celery
from config import config
from raven.contrib.flask import Sentry


# 邮件发送
mail = Mail()
# qiniu管理
qiniu = Qiniu()
iosqn = Qiniu()
# redis静态资源存储~redis1容器~6384端口
# rds = redis.StrictRedis(host='redis1', port=6384, db=0)
rds = redis.StrictRedis(host=os.getenv('REDIS1_HOST'), port=7384, db=0)
# redis通知公告缓存~redis2容器~6381端口
board = redis.StrictRedis(host=os.getenv('REDIS2_HOST'), port=7381, db=0)


def create_app(config_name='default'):
    """
    :function: create_app
    :args:
        - config_name('default'):
            配置的名称, 默认是default
            应用配置具体见 config.py
    :rv:
        - app: restccnu app

    app 工厂函数
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    qiniu.init_app(app)
    iosqn.init_app(app)
    mail.init_app(app)

    from apis import api
    app.register_blueprint(api, url_prefix='/api')

    return app

# restccnu app(flask app)
app = create_app()
# sentry app
sentry = Sentry(app, dsn=os.getenv('DSN_KEY'))


@app.route('/')
def index():
    """
    :function: index
    :args: none
    :rv: html response

    华师匣子下载主页
    """
    return render_template('index.html')

@app.route('/info/')
def info():
    """
    :function: info
    :args: none
    :rv: html response

    华师匣子通知banner
    """
    return render_template('letter.html')

@app.route('/qa/')
def qa():
    """
    :function: qa
    :args: none
    :rv: html response

    华师匣子问答banner
    """
    return render_template('qaindex.html')

@app.route('/h5/')
def h5():
    """
    :function: h5
    :args: none
    :rv: html response

    华师匣子宣传h5
    -- platform = request.user_agent.platform
    """
    platform = request.user_agent.platform
    if platform in ["android", "iphone", "ipad"]:
        return render_template('index_m.html')
    else:
        return render_template('index_d.html')


def make_celery(app):
    """
    :function: make_celery
    :args:
        - app: restccnu app
    :rv: celery实例

    celery工厂函数, 在celery context中实现flask app context,
    方便运行flask任务
    """
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True  # abc
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery
