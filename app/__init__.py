from flask import Flask


def create_app():
    app = Flask(__name__)

    # Importing the blueprints
    from .blueprints.main import main as main_blueprint
    from .blueprints.auth import auth as auth_blueprint

    # Registering the blueprints
    app.register_blueprint(main_blueprint) 
    app.register_blueprint(auth_blueprint)

    return app