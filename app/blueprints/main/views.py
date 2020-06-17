from .forms import EditProfileAdminForm,EditProfileForm
from flask import render_template,redirect,url_for,flash
from flask_login import fresh_login_required,login_required
from ..auth.decorators import permission_required,admin_required
from app.models import Permission,User,Role
from . import main
from app import db

@main.route('/')
@main.route('/home')
def home():
    return render_template('home.html')

@main.route('/fresh-session')
@fresh_login_required
def teste_fresh():
    return "For Fresh Session"

@main.route('/normal-session')
@login_required
def teste_normal():
    return "For Normal Session"

@main.route('/admin')
@login_required
@admin_required
def for_admins_only():
    return "For Admin"

@main.route('/moderate')
@login_required
@permission_required(Permission.MODERATE)
def for_moderates_only():
    return "For Moderates"

@main.app_errorhandler(404)
def error_404(error):
    return render_template('error/404.html'),404

@main.app_errorhandler(500)
def error_500(error):
    return render_template('error/500.html'),500

@main.app_errorhandler(403)
def error_403(error):
    return render_template('error/403.html'),403


@main.route('/user/admin-edit/<int:id>',methods=['GET','POST'])
@login_required
@admin_required
def edit_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user)
    if form.validate_on_submit():
        user.name = form.first_name.data+' '+form.last_name.data
        user.username = form.username.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.change_email(form.email.data)
        db.session.add(user)
        db.session.commit()
        flash('The profile has been updated')
        return redirect(url_for('main.profile',username=user.username))
    return render_template('admin_edit.html',form=form,user=user)

@main.route('/user/<username>')
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('profile.html',user=user)


@main.route('/user/edit',methods=['GET','POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.first_name.data +' '+form.last_name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Profile updated successfuly')
        return redirect(url_for('main.profile',username=current_user.username))

    return render_template('edit_profile.html',form=form)