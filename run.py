from app import create_app
from app import db
from app.models import User,Role


app = create_app('default')

#Stablishing a context to the flask cli

@app.shell_context_processor
def make_shell_context():
    return dict(User=User,Role=Role,db=db)

