 
import os
import secrets
from my_demo_app import limiter, app, cache
from werkzeug.utils import secure_filename
from .form import MultipleFileUploadForm, SingleFileUploadForm
from flask import render_template, Blueprint, redirect, url_for


file_upload_ = Blueprint(
    "file_upload_", __name__, template_folder="templates", static_folder="static"
)


# Route for handling single file upload
@file_upload_.route(f"/{secrets.token_urlsafe()}", methods=["GET", "POST"])
#@file_upload_.route("/singleupload", methods=["GET", "POST"])
@limiter.limit("10 per minute", override_defaults=True)
def secure_single_upload():
    # Create form instance
    form = SingleFileUploadForm()

    # Check if form is submitted and valid
    if form.validate_on_submit():
        # Access the uploaded file
        file = form.file.data

        # Check if a file was uploaded
        if file:
            # Get file extension and lowercase it
            extension = os.path.splitext(file.filename)[1].lower()

            # Generate secure file path
            file_path = os.path.join(
                app.config["UPLOAD_FOLDER"], secure_filename(file.filename)
            )

            # Check if file extension is allowed
            if extension not in app.config["ALLOWED_EXTENSIONS"]:
                return "File is not an allowed type"

            # Save the file to the upload folder
            file.save(file_path)
            
            # Invalidate the cache for the homepage
            with app.app_context():
                cache.delete("home_page")

            # Redirect to registration page after successful upload
            return redirect(url_for("view.home_page"))
        else:
            # Inform user if no file was selected
            return "No file selected"

    # Render the template with the form
    return render_template("file_upload.html", form=form)


# Route for handling multiple file uploads
# @file_upload_.route("/multiple_upload", methods=["GET", "POST"])
# @limiter.limit("10 per minute", override_defaults=True)
# def secure_multiple_upload():
#     # Create form instance
#     form = MultipleFileUploadForm()

#     # Check if form is submitted and valid
#     if form.validate_on_submit():
#         # Access uploaded files as a list
#         files = form.files_.data

#         # Check if any files were uploaded
#         if files:
#             # Loop through each uploaded file
#             for file in files:
#                 # Get file extension and lowercase it
#                 extension = os.path.splitext(file.filename)[1].lower()

#                 # Generate secure file path
#                 file_path = os.path.join(
#                     app.config["UPLOAD_FOLDER"], secure_filename(file.filename)
#                 )

#                 # Check if file extension is allowed
#                 if extension not in app.config["ALLOWED_EXTENSIONS"]:
#                     return "File is not an allowed type"

#                 # Save the file to the upload folder
#                 file.save(file_path)

#             # Redirect to registration page after successful upload
#             return redirect(url_for("view.home_page"))
#         else:
#             # Inform user if no files were selected
#             return "No files selected"

#     # Render the template with the form
#     return render_template("file_upload.html", form=form)

