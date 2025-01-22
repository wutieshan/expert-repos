import flask
from config import Constants as const
from src.db import get_db

blueprint = flask.Blueprint(
    name=const.FLASK_BLUEPRINT_AUTH_NAME,
    import_name=__name__,
    url_prefix=const.FLASK_BLUEPRINT_AUTH_URL_PREFIX,
)


@blueprint.route(const.FLASK_BLUEPRINT_AUTH_REGISTER_ROUTE, methods=["GET", "POST"])
def register():
    if flask.request.method == "POST":
        username = flask.request.form.get("username")
        password = flask.request.form.get("password")

        error = ""
        if not username or not password:
            error += "username or password must not be empty"

        if not error:
            pass

        flask.flash(error)
    return flask.render_template(const.FLASK_BLUEPRINT_AUTH_REGISTER_TEMPLATE)


@blueprint.route("/login", methods=["GET", "POST"])
def login():
    pass


@blueprint.route("/logout", methods=["GET", "POST"])
def logout():
    pass
