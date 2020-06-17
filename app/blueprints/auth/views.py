from flask_login import login_user,logout_user,current_user,login_required
from flask import render_template,url_for,redirect,flash,request
from .forms import RegistrationForm,LoginForm
from urllib.parse import urlparse,urljoin
from app.models import User
from . import auth
from app import db
from .email import send_message

def url_is_safe(target_url):
    host_url = urlparse(request.host_url)
    next_url = urlparse(urljoin(request.host_url,target_url))
    return host_url.scheme in ('http','https') and host_url.netloc == next_url.netloc


@auth.route('/register',methods=['GET','POST'])
def register():
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
        token = user.generate_confirmation_token()
        send_message('Confirm Account',form.email.data,'email/confirm/email',user=user,token=token)
        flash('An email to confirm your account was sent to you')
        return redirect(url_for('auth.login'))
    return render_template('register.html',form=form)

@auth.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.find_by_email(form.email.data)
        if not user:
            flash('Invalid email or password')
        else:
            if not user.confirmed:
                flash('Confirm your account first')
            elif user.check_password(form.password.data):
                user.create_session_token()
                login_user(user,remember=form.remember_me.data)
                flash('Logged in successfuly')
                next_url = request.args.get('next')
                return redirect(next_url) if next_url and url_is_safe(next_url) else redirect(url_for('main.home'))
        return redirect(url_for('auth.login'))
    return render_template('login.html',form=form)
        
    

@auth.route('/logout')
@login_required
def logout():
    current_user.remove_session_token()
    logout_user()
    flash('Logout successfuly')
    return redirect(url_for('main.home'))

@auth.route('/confirm/<token>')
def confirm_account(token):
    confirm = User.confirm_account(token)
    if confirm:
        flash('You confirmed your account! Now you can Log In')
    else:
        flash('Invalid or expired token')
    return redirect(url_for('auth.login'))


@auth.before_app_request
def before_each_request():
    if current_user.is_authenticated:
        current_user.ping()

