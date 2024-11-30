
import secrets
from my_demo_app import limiter
from flask import render_template, Blueprint


authent_ = Blueprint(
    "authent_", __name__, template_folder="templates", static_folder="static"
)


@authent_.route(f"/{secrets.token_urlsafe()}")
@limiter.limit("5 per minute", override_defaults=True)
def secure_register():
    return render_template("signup.html")


@authent_.route(f"/{secrets.token_urlsafe()}")
@limiter.limit("5 per minute", override_defaults=True)
def secure_login():
    return render_template("login.html")


# route can be define and render without using secrets & limiter module but using it add more robustness to your route and application 
# @authent_.route("/login")
# def secure_login():
#     return render_template("login.html")
