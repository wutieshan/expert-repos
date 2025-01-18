import click
import flask
from db import get_db
from config import Constants as const


@click.command("init-db")
def init_db():
    db = get_db()

    with flask.current_app.open_resource(const.FLASK_DB_DDL_PATH) as fp:
        sqltext = fp.read().decode("utf8")
        click.echo(f"{sqltext=}")
        db.executescript(str.replace(sqltext, "\r\n", " "))
    
    with flask.current_app.open_resource(const.FLASK_DB_DML_PATH) as fp:
        sqltext = fp.read().decode("utf8")
        click.echo(f"{sqltext=}")
        db.executescript(sqltext)
    
    click.echo("database initialized successfully.")


def init_app(app):
    app.cli.add_command(init_db)
