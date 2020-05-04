from flask import Flask

from citizens.handlers.imports import imports


def create_app():
    app = Flask(__name__)
    app.register_blueprint(imports, url_prefix='/imports')
    return app
