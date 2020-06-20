from flask import request,render_template,jsonify
from . import main


@main.app_errorhandler(404)
def error_404(error):
    if request.accept_mimetypes.accept_json and \
        not request.accept_mimetypes.accept_html:
        response = jsonify({'error':'not found'})
        response.status_code = 404
        return response
    return render_template('error/404.html'),404

@main.app_errorhandler(500)
def error_500(error):
    if request.accept_mimetypes.accept_json and \
        not request.accept_mimetypes.accept_html:
        response = jsonify({'error':'internal server error'})
        response.status_code = 500
        return response
    return render_template('error/500.html'),500

@main.app_errorhandler(403)
def error_403(error):
    return render_template('error/403.html'),403