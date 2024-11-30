 
import os
import secrets
from PIL import Image
from my_demo_app import app
from flask import Blueprint
from flask_login import current_user


img_utils = Blueprint(
    "img_utils", __name__, template_folder="templates", static_folder="static"
)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        app.root_path, "static/profile_pics", picture_fn
    )  # app.
    if os.path.exists(
        app.root_path + "/static/media/" + current_user.user_profile
    ):
        os.remove(app.root_path + "/static/media/" + current_user.user_profile)

    output_size = (100, 100)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn
