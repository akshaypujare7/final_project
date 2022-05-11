from flask import render_template
import flask
import logging

error_handlers = flask.Blueprint('error_handlers', __name__)


@error_handlers.app_errorhandler(404)
def page_not_found(e):
    log = logging.getLogger("errors")
    log.info("404: Page not Found")
    return render_template("404.html"), 404
