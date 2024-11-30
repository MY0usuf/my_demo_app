 
from flask_wtf import FlaskForm
from flask_login import current_user
from my_demo_app.database.models import User
from wtforms import StringField, SubmitField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, ValidationError


class UpdateAccount(FlaskForm):
    username = StringField(validators=[DataRequired()])
    picture = FileField(
        label="Update account profile", validators=[FileAllowed(["jpg", "png"])]
    )
    submit = SubmitField(label="Update")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    "That username already exist! Please try a different username"
                )
