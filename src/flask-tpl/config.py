import os


class Constants:
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    PROJECT_DATA_DIR = os.path.join(PROJECT_ROOT, "data")
    PROJECT_CONFIG_DIR = os.path.join(PROJECT_ROOT, "conf")

    FLASK_INSTANCE_PATH = os.path.join(PROJECT_ROOT, "instance")
    FLASK_SECRET_KEY = "dev-tieshan"

    FLASK_DB_PATH = os.path.join(FLASK_INSTANCE_PATH, "flask.sqlite3")
    FLASK_DB_GLOBAL_NAME = "flaskdb"
    FLASK_DB_DDL_PATH = os.path.join(PROJECT_DATA_DIR, "schema-ddl.sql")
    FLASK_DB_DML_PATH = os.path.join(PROJECT_DATA_DIR, "schema-dml.sql")

    FLASK_CLICK_CMD_INIT_DB = "init-db"

    FLASK_BLUEPRINT_AUTH_NAME = "auth"
    FLASK_BLUEPRINT_AUTH_URL_PREFIX = "/auth"
    FLASK_BLUEPRINT_AUTH_REGISTER_ROUTE = "/register"
    FLASK_BLUEPRINT_AUTH_REGISTER_TEMPLATE = "auth/register.html"

    FLASK_CONFIG_APP_LOG_PATH = os.path.join(FLASK_INSTANCE_PATH, "app", "log.json")


class Config:
    pass


if __name__ == "__main__":
    print(Constants.PROJECT_ROOT)
