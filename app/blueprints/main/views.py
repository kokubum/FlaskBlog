from flask_login import fresh_login_required,login_required
from ..auth.decorators import permission_required,admin_required
from app.models import Permission
from flask import render_template
from . import main

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
