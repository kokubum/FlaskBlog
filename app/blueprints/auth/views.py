from flask import render_template,url_for
from . import auth


@auth.route('/register')
def sign_up():
    return render_template('register.html')

@auth.route('/login')
def login():
    return render_template('login.html')