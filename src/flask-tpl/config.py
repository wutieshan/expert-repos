import os


class Constants:
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

    FLASK_INSTANCE_PATH = os.path.join(PROJECT_ROOT, "instance")
    FLASK_SECRET_KEY = "dev-tieshan"
    FLASK_SQLITE3_PATH = os.path.join(FLASK_INSTANCE_PATH, "flask.sqlite3")

    DB_DDL_PATH = os.path.join(PROJECT_ROOT, "db", "schema-ddl.sql")
    DB_DML_PATH = os.path.join(PROJECT_ROOT, "db", "schema-dml.sql")


class Config:
    pass


if __name__ == "__main__":
    print(Constants.PROJECT_ROOT)
