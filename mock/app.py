# coding: utf-8

from flask import Flask


def create_app():
    app = Flask(__name__)

    from apis import api
    app.register_blueprint(api, url_prefix='/api')

    return app


app = create_app()
