from flask import render_template,url_for
from .forms import RegistrationForm,LoginForm
from . import auth


@auth.route('/register',methods=['GET','POST'])
def sign_up():
    form = RegistrationForm()
    return render_template('register.html',form=form)

@auth.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html',form=form)