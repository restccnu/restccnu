# coding: utf-8

import redis
from flask import Flask


# Initial redis for table store
rds = redis.StrictRedis(host='localhost', port=6379, db=0)


def create_app():
    app = Flask(__name__)

    from apis import api
    app.register_blueprint(api, url_prefix='/api')

    return app


app = create_app()
