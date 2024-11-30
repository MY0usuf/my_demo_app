
from sqlalchemy import or_
from my_demo_app import limiter
from .form import ProductSearchForm
from my_demo_app.database.models import User
from flask import render_template, Blueprint, flash


search_ = Blueprint(
    "search_", __name__, template_folder="templates", static_folder="static"
)


@search_.route("/search")
@limiter.limit("5 per minute", override_defaults=True)
def search_item():
    form = ProductSearchForm()
    search_results = []  # Intialize early to avoid UnboundLocalError

    if form.validate_on_submit():
        search_query = form.search_query.data
        search_results = User.query.filter(
            User.username.ilike(f"%{search_query}%")
        ).all()
        if search_results:
            flash(
                message=f"{len(search_query)}Data found for query: {search_query}",
                category="success",
            )
        else:
            flash(message=f"Data not found for query: {search_query}", category="error")
    return render_template("item_search.html", form=form, search_results=search_results)
