
import secrets
from flask import render_template, Blueprint


admin_controller = Blueprint(
    "admin_controller", __name__, template_folder="templates", static_folder="static"
)
                              

# @admin_controller.route(f"/{secrets.token_urlsafe()}")
@admin_controller.route("/controller", methods=["GET"])
def controller():
    return render_template("controller.html")
