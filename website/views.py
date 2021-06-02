from website import create_app
from flask import render_template, Blueprint

views = Blueprint('views', __name__)

app = create_app()


@views.route('/')
def home():
    return render_template('home.html')

