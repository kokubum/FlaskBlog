from flask import render_template,url_for,redirect,flash
from app.models import User
from .forms import RegistrationForm,LoginForm
from . import auth
from app import db



@auth.route('/register',methods=['GET','POST'])
def sign_up():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            name = form.first_name.data+' '+form.last_name.data,
            email = form.email.data,
            username = form.username.data,
            password = form.password.data

        )
        db.session.add(user)
        db.session.commit()
        flash('You now can log in!')
        return redirect(url_for('auth.login'))
    return render_template('register.html',form=form)

@auth.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html',form=form)