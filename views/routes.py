
import os
from my_demo_app import app, cache
from my_demo_app.caching.cache_constant import FOUR_MINUTES
from flask import render_template, Blueprint, send_from_directory, abort


view = Blueprint("view", __name__, template_folder="templates", static_folder="static")


@view.route("/")
@cache.cached(timeout=FOUR_MINUTES, key_prefix="home_page")
def home_page():
    # This function retrieves a list of allowed image filenames and renders the homepage template.

    # Get list of all files in the upload folder
    files = os.listdir(app.config["UPLOAD_FOLDER"])

    # Create an empty list to store allowed image filenames
    images = []

    # Loop through each file in the upload folder
    for file in files:
        # Extract the file extension and convert it to lowercase
        extention = os.path.splitext(file)[1].lower()

        # Check if the extension is allowed (e.g., ".jpg", ".png")
        if extention in app.config["ALLOWED_EXTENSIONS"]:
            # If the extension is allowed, add the filename to the images list
            images.append(file)

    # Render the homepage template and pass the list of images
    return render_template("index.html", images=images)


# @view.route("/")
# def home_page():
#     # This function retrieves a list of allowed image filenames using list comprehension and renders the homepage template.

#     # Get list of all files in the upload folder
#     files = os.listdir(app.config["UPLOAD_FOLDER"])

#     # Use list comprehension to filter allowed image filenames based on extension
#     images = [file for file in files if os.path.splitext(file)[1].lower() in app.config["ALLOWED_EXTENSIONS"]
#     ]

#     # Render the homepage template and pass the list of images
#     return render_template("index.html", images=images)


@view.route("/serve-image/<filename>", methods=["GET"])
def serve_image(filename):
    # This function serves an image from the uploads folder based on the provided filename in the URL.

    # Construct the full path to the image file
    image_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    # Check if the requested image file exists
    if not os.path.isfile(image_path):

        # Abort the request with a 404 Not Found status code
        abort(404)

    # Use Flask's send_from_directory utility to serve the image
    return send_from_directory(directory=app.config["UPLOAD_FOLDER"], path=filename)
