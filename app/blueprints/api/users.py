from app.models import Post,Permission,Comment,User,Follow
from flask import jsonify,url_for,request,current_app,g
from .decorators import permission_required
from . errors import forbidden
from . import api

@api.route('/users/<int:id>/')
def get_user(id):
    user = User.query.get_or_404(id)  
    return jsonify(user.to_json())


@api.route('/users/<int:id>/posts/')
def get_user_posts(id):
    user = User.query.get_or_404(id)
    page = request.args.get('page',1,type=int)
    pagination = user.posts.order_by(Post.time_stamp.desc()).paginate(
        page,
        per_page = current_app.config['POSTS_PER_PAGE'],
        error_out = False
    )
    posts = pagination.items
    prev = None
    if pagination.has_prev:
        prev=url_for('api.get_user_posts',id=id,page=page-1)
    next = None
    if pagination.has_next:
        next = url_for('api.get_user_posts',id=id,page=page+1)
    return jsonify({
        'posts:':[post.to_json() for post in posts],
        'prev_url':prev,
        'next_url':next,
        'count':pagination.total
        }
    )
    return jsonify({'posts':[post.to_json() for post in posts]})

@api.route('/users/<int:id>/timeline/')
def get_user_followed_posts(id):
    user = User.query.get_or_404(id)
    if g.current_user != user:
        return forbidden('Insufficient permissions')
    page = request.args.get('page', 1, type=int)
    pagination = user.followed_posts.order_by(Post.time_stamp.desc()).paginate(
        page, per_page=current_app.config['POSTS_PER_PAGE'],
        error_out=False
    )
    posts = pagination.items
    print(pagination.items)
    print(pagination.next().items)
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_user_followed_posts', id=id, page=page-1)
    next = None
    if pagination.has_next:
        next = url_for('api.get_user_followed_posts', id=id, page=page+1)
    return jsonify({
        'posts': [post.to_json() for post in posts],
        'prev': prev,
        'next': next,
        'count': pagination.total
        }
    )