# coding: utf-8

import redis
from flask import Flask
from config import config


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    from apis import api
    app.register_blueprint(api, url_prefix='/api')

    return app


app = create_app()
