from .forms import EditProfileAdminForm,EditProfileForm,PostForm
from flask import render_template,redirect,url_for,flash,current_app,request
from flask_login import fresh_login_required,login_required
from ..auth.decorators import permission_required,admin_required
from app.models import Permission,User,Role,Post
from . import main
from app import db

@main.route('/')
@main.route('/home')
def home():

    page = request.args.get('page',1,type=int)
    pagination = Post.query.order_by(Post.time_stamp.desc()).paginate(
        page,
        per_page = current_app.config['POSTS_PER_PAGE'],
        error_out=False
    )
    posts = pagination.items
    return render_template('home.html',posts=posts,pagination=pagination)


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

@main.route('/post',methods=['GET','POST'])
@login_required
@permission_required(Permission.WRITE)
def post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title = form.title.data,
            body = form.body.data,
            author = current_user._get_current_object()
        )
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.home'))
    return render_template('post.html',form=form)