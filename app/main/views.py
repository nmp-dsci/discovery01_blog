from flask import render_template, url_for
from . import main


@main.route('/',methods=['GET'])
def home():
    return render_template('home.html')

