from itsdangerous import URLSafeTimedSerializer as Serializer
from flask_login import UserMixin
from app import db, bcrypt,login_manager
from flask import current_app


@login_manager.user_loader
def load_user(user_token):
    return User.find_by_session(user_token)


class User(db.Model,UserMixin):

    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),nullable=False) 
    email = db.Column(db.String(40),unique=True,nullable=False,index=True)
    username = db.Column(db.String(40),unique=True,nullable=False,index=True)
    password_hash = db.Column(db.String(64),nullable=False)
    session_token = db.Column(db.String(100))

    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))

    @property
    def password():
        raise AttributeError("You can't acess the password")

    @password.setter
    def password(self,password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self,password):
        return bcrypt.check_password_hash(self.password_hash,password)

    def get_id(self):
        return self.session_token

    def create_session_token(self):
        serial = Serializer(current_app.config['SECRET_KEY'])
        self.session_token = serial.dumps([self.id,self.password_hash])

        db.session.commit()
    
    def remove_session_token(self):
        self.session_token = None
        
        db.session.commit()

    @classmethod
    def find_by_email(cls,email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_username(cls,username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_session(cls,session_token):
        return cls.query.filter_by(session_token=session_token).first()

class Role(db.Model):

    __tablename__ = 'roles'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20),unique=True,nullable=False)

    users = db.relationship('User',backref='role',lazy='dynamic')


