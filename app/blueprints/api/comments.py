from flask import jsonify,current_app,request,g,url_for
from app.models import Comment
from . import api

@api.route('/comments/')
def get_comments():
    page = request.args.get('page',1,type=int)
    pagination = Comment.query.order_by(Comment.time_stamp.desc()).paginate(
        page,
        per_page = current_app.config['COMMENTS_PER_PAGE'],
        error_out = False
    )
    comments = pagination.items
    prev = None
    if pagination.has_prev:
        prev=url_for('api.get_comments',page=page-1)
    next = None
    if pagination.has_next:
        next = url_for('api.get_comments',page=page+1)
    return jsonify({
        'comments:':[comment.to_json() for comment in comments],
        'prev_url':prev,
        'next_url':next,
        'count':pagination.total
        }
    )

@api.route('/comments/<int:id>/')
def get_comment(id):
    comment = Comment.query.get_or_404(id)
    return jsonify(comment.to_json())
