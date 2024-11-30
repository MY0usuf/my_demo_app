
import secrets
from my_demo_app import db
from .form import UpdateAccount
from flask import render_template, Blueprint


account_ = Blueprint(
    "account_", __name__, template_folder="templates", static_folder="static"
)


#@account_.route(f"/{secrets.token_urlsafe()}")
@account_.route("/reset", methods=["GET"])
def secure_password():
    return render_template("reset_pswd.html")


@account_.route(f"/{secrets.token_urlsafe()}")
def secure_account_update():
    return render_template("update_account.html")
