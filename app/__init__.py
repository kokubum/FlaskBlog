from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask import Flask
from config import config

db = SQLAlchemy()
bcrypt = Bcrypt()


#Factory of the application
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    #Initializing the extensions
    db.init_app(app)
    bcrypt.ini_app(app)

    # Importing the blueprints
    from .blueprints.main import main as main_blueprint
    from .blueprints.auth import auth as auth_blueprint

    # Registering the blueprints
    app.register_blueprint(main_blueprint) 
    app.register_blueprint(auth_blueprint)

    return app