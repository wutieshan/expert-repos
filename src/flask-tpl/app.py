import flask
import os
from config import Constants as const


def app_factory():
    app = flask.Flask(
        __name__,
        instance_path=const.FLASK_INSTANCE_PATH,
    )

    app.config.from_mapping(
        SECRET_KEY=const.FLASK_SECRET_KEY,
        DATABASE=const.FLASK_SQLITE3_PATH,
    )
    app.config.from_mapping()

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from commands import init_app

    init_app(app)

    return app
