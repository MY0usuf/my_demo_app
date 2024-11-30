
from flask import session
from my_demo_app import app
from http import HTTPStatus
from flask import render_template, Blueprint, flash


errors_ = Blueprint(
    "errors_", __name__, template_folder="templates", static_folder="static"
)


@errors_.app_errorhandler(403)
def forbidden_error(error):
    return render_template("forbidden.html"), HTTPStatus.FORBIDDEN


@errors_.app_errorhandler(404)
def not_found_error(error):
    return render_template("not_found.html"), HTTPStatus.NOT_FOUND


@errors_.app_errorhandler(413)
def payload_too_large_error(error):
    return render_template("payload_data.html"), HTTPStatus.PAYLOAD_TOO_LARGE


@errors_.app_errorhandler(429)
def too_many_requests_error(error):
    flash(
        message="Your request is too much, try again in a few minutes", category="error"
    )
    return render_template("too_many_requests.html"), HTTPStatus.TOO_MANY_REQUESTS


@errors_.app_errorhandler(500)
def internal_server_error(error):
    return (
        render_template("internal_server.html"),
        HTTPStatus.INTERNAL_SERVER_ERROR,
    )


@errors_.app_errorhandler(ValueError)
def value_error(error):
    error_message = session.pop("error_message", None)
    if error_message:
        app.logger.error(error_message)
    else:
        app.logger.error(f"Error occurred: {error}")
    return render_template("invalid_path.html")


def maintainance():
    # Your logic here
    pass


@errors_.app_errorhandler(503)
def app_maintenance_mode(error):  # Optional prefix for consistency
    if maintainance:  # Replace with your logic to check maintenance mode
        return render_template("maintenance.html"), HTTPStatus.SERVICE_UNAVAILABLE
    # Code to handle other 503 errors (optional)
    return None  # Fallback for non-maintenance related 503 errors

