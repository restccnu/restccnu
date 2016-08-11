# coding: utf-8

import redis
from flask import Flask
from flask_zero import Qiniu
from celery import Celery
from config import config


qiniu = Qiniu()
rds = redis.StrictRedis(host='localhost', port=6384, db=0)
board = redis.StrictRedis(host='localhost', port=6381, db=0)


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    qiniu.init_app(app)

    from apis import api
    app.register_blueprint(api, url_prefix='/api')

    return app


app = create_app()


def make_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery
