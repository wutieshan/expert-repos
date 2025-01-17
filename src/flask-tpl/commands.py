import click
from db import SQLiteProxy
from config import Constants as const


@click.command("init-db")
def init_db():
    proxy = SQLiteProxy(const.FLASK_SQLITE3_PATH)
    proxy.executescript(const.DB_DDL_PATH)
    proxy.executescript(const.DB_DML_PATH)
    click.echo("database initialized successfully.")


def init_app(app):
    app.cli.add_command(init_db)
