import flask
from config import Constants as const

from ._base import Proxy
from .sqlite import SQLiteOptions, SQLiteProxy


def get_db() -> Proxy:
    # TODO: to be renovated, use a more elegant way to choose different types of database

    FLASK_DB_GLOBAL_NAME = const.FLASK_DB_GLOBAL_NAME

    if hasattr(flask.g, FLASK_DB_GLOBAL_NAME):
        return getattr(flask.g, FLASK_DB_GLOBAL_NAME)

    options = SQLiteOptions()
    options.dbpath = const.FLASK_DB_PATH

    proxy = SQLiteProxy(options)
    setattr(flask.g, FLASK_DB_GLOBAL_NAME, proxy.get_conn())
    return getattr(flask.g, FLASK_DB_GLOBAL_NAME)
