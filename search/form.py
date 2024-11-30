 
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import SearchField, SubmitField


class ProductSearchForm(FlaskForm):
    search_query = SearchField(validators=[DataRequired()], render_kw={"placeholder": "Search product name"})
    submit = SubmitField(label="Search")
