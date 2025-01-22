import click
import flask
from db import get_db
from config import Constants as const


@click.command("init-db")
def init_db():
    db = get_db()

    with open(const.FLASK_DB_DDL_PATH, "r", encoding="utf8") as fp:
        db.executescript(fp.read())
    
    with open(const.FLASK_DB_DML_PATH, "r", encoding="utf8") as fp:
        db.executescript(fp.read())

    click.echo("database initialized successfully.")


def init_app(app):
    app.cli.add_command(init_db)
