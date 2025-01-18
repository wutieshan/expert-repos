import flask
from ._sqlite import SQLiteProxy
from config import Constants as const

def get_db() -> SQLiteProxy:
    FLASK_DB_GLOBAL_NAME = const.FLASK_DB_GLOBAL_NAME

    if hasattr(flask.g, FLASK_DB_GLOBAL_NAME):
        return getattr(flask.g, FLASK_DB_GLOBAL_NAME)
    
    proxy = SQLiteProxy(const.FLASK_DB_PATH)
    setattr(flask.g, FLASK_DB_GLOBAL_NAME, proxy.connect())
    return getattr(flask.g, FLASK_DB_GLOBAL_NAME)