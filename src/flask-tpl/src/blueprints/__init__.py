import flask
from .auth import auth


def register_blueprints(app: flask.Flask):
    app.register_blueprint(auth.blueprint)
