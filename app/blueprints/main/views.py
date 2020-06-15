from flask import render_template
from . import main

@main.route('/')
@main.route('/home')
def home():
    return render_template('home.html')

@main.app_errorhandler(404)
def error_404(error):
    return render_template('error/404.html'),404

@main.app_errorhandler(505)
def error_505(error):
    return render_template('error/505.html'),505
