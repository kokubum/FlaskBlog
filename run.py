from app.models import User,Role,Post,Comment,Permission
from flask_migrate import Migrate
from app import create_app
from app import db
import os

app = create_app(os.environ.get('CONFIG_TYPE','default'))

migrate = Migrate(app,db)


#Stablishing a context to the flask cli
@app.shell_context_processor
def make_shell_context():
    return dict(User=User,Role=Role,Post=Post,Comment=Comment,db=db)

#Stablishing a common variable to the context of the template
@app.context_processor
def inject_permission():
    return dict(Permission=Permission)

