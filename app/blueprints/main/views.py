from .forms import EditProfileAdminForm,EditProfileForm,PostForm,CommentForm,EditPostForm
from flask import render_template,redirect,url_for,flash,current_app,request,abort,make_response
from flask_login import fresh_login_required,login_required,current_user
from ..auth.decorators import permission_required,admin_required
from app.models import Permission,User,Role,Post,Comment,Follow
from datetime import datetime
from . import main
from app import db

@main.route('/')
@main.route('/home')
def home():

    show_followed=False
    if current_user.is_authenticated:
        show_followed = bool(request.cookies.get('show_followed',''))
    
    if show_followed:
        query = current_user.followed_posts
    else:
        query = Post.query

    page = request.args.get('page',1,type=int)
    pagination = query.order_by(Post.time_stamp.desc()).paginate(
        page,
        per_page = current_app.config['POSTS_PER_PAGE'],
        error_out=False
    )
    posts = pagination.items
    return render_template(
        'home.html',
        posts=posts,
        pagination=pagination,
        show_followed=show_followed,
        endpoint='main.home'
        )

@main.route('/all')
@login_required
def show_all():
    resp = make_response(redirect(url_for('main.home')))
    resp.set_cookie('show_followed','',max_age=30*24*60*60)
    return resp

@main.route('/followed')
@login_required
def followed():
    resp = make_response(redirect(url_for('main.home')))
    resp.set_cookie('show_followed','1',max_age=30*24*60*60)
    return resp

@main.route('/post/<int:id>',methods=['GET','POST'])
def show_post(id):
    
    post = Post.query.filter_by(id=id).first()
    form = CommentForm()
    if form.validate_on_submit():
        if current_user.can(Permission.COMMENT):
            comment = Comment(
                body = form.body.data,
                time_stamp = datetime.utcnow(),
                author = current_user._get_current_object(),    
                post = post
            )
            db.session.add(comment)
            db.session.commit()
        else:
            flash('You don\'t have permission to comment')
        return redirect(url_for('main.show_post',id=post.id,page=-1))
    page = request.args.get('page',1,type=int)
    if page == -1:
        page = ((post.comments.count() - 1)//current_app.config['COMMENTS_PER_PAGE'])+1 
    pagination = post.comments.order_by(Comment.time_stamp.asc()).paginate(
        page,
        per_page = current_app.config['COMMENTS_PER_PAGE'],
        error_out = False
    )
    
    comments = pagination.items
    enable_comments = post.comments.filter_by(disabled=False).count()
    return render_template(
        'show_post.html',
        post=post,
        comments=comments,
        form=form,
        pagination=pagination,
        endpoint='main.show_post',
        enable_comments = enable_comments,
        page=page
        )


@main.route('/post/<int:id>/edit-post',methods=['GET','POST'])
@login_required
def edit_post(id):
    post = Post.query.filter_by(id=id).first()
    if current_user != post.author and not current_user.is_admin():
        abort(403)
    form = EditPostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        db.session.add(post)
        db.session.commit()
        flash('The post has been updated')
        return redirect(url_for('main.show_post',id=id))
    form.body.data = post.body_html
    return render_template('edit_post.html',form=form,post=post)


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

@main.route('/follow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
    user = User.find_by_username(username)
    if user and current_user!=user:
        current_user.follow(user)
        return redirect(url_for('main.profile',username=username))
    return redirect(url_for('main.home'))

@main.route('/unfollow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(username):
    user = User.find_by_username(username)
    if user and current_user!=user:
        current_user.unfollow(user)
        return redirect(url_for('main.profile',username=username))
    return redirect(url_for('main.home'))

@main.route('/followers/<username>')
def followers(username):
    user = User.find_by_username(username)
    if user is None:
        flash('Invalid User')
        return redirect(url_for('main.home'))
    page = request.args.get('page',1,type=int)
    pagination = user.follower.filter(Follow.follower_id!=user.id).paginate(
        page,
        per_page = current_app.config['FOLLOWERS_PER_PAGE'],
        error_out=False
    )
    follows = [{'user':item.follower,'time_stamp':item.time_stamp} for item in pagination.items]
    return render_template(
        'followers.html',
        followers=follows,
        user=user,
        title="Followers Of",
        endpoint='main.followers',
        pagination=pagination
    )

@main.route('/followed-by/<username>')
def followed_by(username):
    user = User.find_by_username(username)
    if user is None:
        flash('Invalid User')
        return redirect(url_for('main.home'))
    page = request.args.get('page',1,type=int)
    pagination = user.followed.filter(Follow.followed_id!=user.id).paginate(
        page,
        per_page = current_app.config['FOLLOWERS_PER_PAGE'],
        error_out=False
    )
    follows = [{'user':item.followed,'time_stamp':item.time_stamp} for item in pagination.items]
    return render_template(
        'followers.html',
        followers=follows,
        user=user,
        title="Followed By",
        endpoint='main.followed_by',
        pagination=pagination
    )

@main.route('/moderate')
@login_required
@permission_required(Permission.MODERATE)
def moderate():
    page = request.args.get('page',1,type=int)
    pagination = Comment.query.order_by(Comment.time_stamp.desc()).paginate(
        page,
        per_page = current_app.config['COMMENTS_PER_PAGE'],
        error_out=False
    )
    comments = pagination.items
    return render_template(
        'moderate.html',
        comments=comments,
        pagination=pagination,
        endpoint='main.moderate',
        page=page
    )

@main.route('/moderate/enable/<int:id>')
@login_required
@permission_required(Permission.MODERATE)
def moderate_disable(id):

    comment = Comment.query.get_or_404(id)
    comment.disabled = True
    db.session.add(comment)
    db.session.commit()
    page = request.args.get('page',1,type=int)
    if request.args.get('post_page'):
        return redirect(url_for('main.show_post',id=comment.post_id,page=page))

    return redirect(url_for('main.moderate',page=page))

@main.route('/moderate/disable/<int:id>')
@login_required
@permission_required(Permission.MODERATE)
def moderate_enable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = False
    db.session.add(comment)
    db.session.commit()
    page = request.args.get('page',1,type=int)
    if request.args.get('post_page'):
        return redirect(url_for('main.show_post',id=comment.post_id,page=page))
    return redirect(url_for('main.moderate',page=page))

@main.app_errorhandler(404)
def error_404(error):
    return render_template('error/404.html'),404

@main.app_errorhandler(500)
def error_500(error):
    return render_template('error/500.html'),500

@main.app_errorhandler(403)
def error_403(error):
    return render_template('error/403.html'),403