from flask_login import login_required,current_user
from flask import render_template,url_for,redirect
from app.models import User
from .forms import EditProfileForm
from . import user
from app import db

@user.route('/<username>')
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('profile.html',user=user)


@user.route('/edit',methods=['GET','POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.first_name.data +' '+form.last_name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        return redirect(url_for('user.profile',username=current_user.username))

    return render_template('edit_profile.html',form=form)