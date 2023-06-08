from flask import Blueprint, render_template, url_for
from transcript_api.resources.routes import api
main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    return render_template('home.html')


@main.route('/online')
def online():
    return {"online" : "yes"}, 200