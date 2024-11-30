 
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from flask_wtf.file import FileField, MultipleFileField, DataRequired


class SingleFileUploadForm(FlaskForm):
    file = FileField(label="Select File", validators=[DataRequired()])
    submit = SubmitField("Submit")


class MultipleFileUploadForm(FlaskForm):
    files_ = MultipleFileField(label="Select files", validators=[DataRequired()])
    submit = SubmitField(label="Submit")
