from flask import Blueprint, render_template
from flask_login import login_required, current_user

routes = Blueprint('routes', __name__)

@routes.route('/', methods=['GET', 'POST'])
@login_required
def home():
    """
    Render the home page.
    Requires the user to be logged in.
    """
    return render_template("home.html", user=current_user)
