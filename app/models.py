from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin,AnonymousUserMixin
from flask import current_app,request,url_for
from app import db, bcrypt,login_manager
from app.exceptions import ValidationError
from datetime import datetime
from markdown import markdown
import hashlib
import bleach

@login_manager.user_loader
def load_user(user_token):
    user = User.find_by_session(user_token)
    if user and user.token_expire():
        user.remove_session_token()
        return None
    return user

class Follow(db.Model):
    __tablename__ = 'followers'
    id = db.Column(db.Integer,primary_key=True)
    follower_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    followed_id = db.Column(db.Integer,db.ForeignKey('users.id'))

    time_stamp = db.Column(db.DateTime,default=datetime.utcnow)

class User(db.Model,UserMixin):

    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),nullable=False) 
    email = db.Column(db.String(40),unique=True,nullable=False,index=True)
    username = db.Column(db.String(40),unique=True,nullable=False,index=True)
    password_hash = db.Column(db.String(64),nullable=False)
    confirmed = db.Column(db.Boolean,default=False)
    session_token = db.Column(db.String(100))

    #profile informations
    about_me = db.Column(db.Text())
    location = db.Column(db.String(64))
    member_since = db.Column(db.DateTime(),default = datetime.utcnow)
    last_seen = db.Column(db.DateTime(),default = datetime.utcnow)

    #avatar
    avatar_hash = db.Column(db.String(40))

    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    posts = db.relationship('Post',backref='author',lazy='dynamic',cascade='all,delete-orphan')
    comments = db.relationship('Comment',backref='author',lazy='dynamic',cascade='all,delete-orphan')

    followed = db.relationship(
        'Follow',
        foreign_keys=[Follow.follower_id],
        backref = db.backref('follower',lazy='joined'),
        lazy='dynamic',
        cascade = 'all,delete-orphan'
    )
    follower = db.relationship(
        'Follow',
        foreign_keys=[Follow.followed_id],
        backref = db.backref('followed',lazy='joined'),
        lazy='dynamic',
        cascade = 'all,delete-orphan'
    )


    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['ADMIN_BLOG']:
                self.role = Role.query.filter_by(name='Administrator').first()
            else:
                self.role = Role.query.filter_by(default=True).first()
            self.avatar_hash = self.gravatar_hash()

    def to_json(self):
        json_user =  {
            'url':url_for('api.get_user',id=self.id),
            'username':self.username,
            'member_since':self.member_since,
            'last_seen':self.last_seen,
            'posts_url':url_for('api.get_user_posts',id=self.id),
            'follower_posts_url':url_for('api.get_user_followed_posts',id=self.id),
            'post_count':self.posts.count()
        }
        return json_user

    def generate_auth_token(self,expiration):
        s = Serializer(current_app.config['SECRET_KEY'],expires_in=expiration)
        return s.dumps({'id':self.id}).decode('utf-8')

    @staticmethod
    def check_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.find_by_id(data['id'])


    @property
    def followed_posts(self):
        return Post.query.join(Follow,Follow.followed_id==Post.author_id).filter(Follow.follower_id==self.id)


    def change_email(self,email):
        if email != self.email:
            self.email = email
            self.avatar_hash = self.gravatar_hash()

    def follow(self,user):
        if not self.is_following(user) :
            f = Follow(follower = self,followed=user)
            db.session.add(f)
            db.session.commit()
    
    def unfollow(self,user):
        f = self.followed.filter_by(followed_id=user.id).first()
        if f:
            db.session.delete(f)
            db.session.commit()

    def is_following(self,user):
        return self.followed.filter_by(followed_id=user.id).first() is not None


    def is_followed_by(self,user):
        return self.followers.filter_by(follower_id=user.id).first() is not None


    def gravatar_hash(self):
        return hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()

    def gravatar(self,size=100,default='identicon',rating='g'):
        if request.is_secure:
            url='https://secure.gravatar.com/avatar'
        else:
            url='http://www.gravatar.com/avatar'
        hash = self.avatar_hash
        return f'{url}/{hash}?s={size}&d={default}&r={rating}'


    @property
    def password():
        raise AttributeError("You can't acess the password")

    @password.setter
    def password(self,password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self,password):
        return bcrypt.check_password_hash(self.password_hash,password)

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def can(self,perm):
        return self.role.has_permission(perm)
    
    def is_admin(self):
        return self.can(Permission.ADMIN)

    def generate_recover_token(self,expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'],expiration)
        return s.dumps({'recover':self.id}).decode('utf-8')

    def generate_confirmation_token(self,expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'],expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    def get_id(self):
        return self.session_token

    def create_session_token(self,expiration=300):
        s = Serializer(current_app.config['SECRET_KEY'],expiration)
        self.session_token = s.dumps({'session_token':[self.id,self.password_hash]}).decode('utf-8')

        db.session.commit()
    
    def remove_session_token(self):
        self.session_token = None
        
        db.session.add(self)
        db.session.commit()

    def token_expire(self):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(self.session_token.encode('utf-8'))
        except:
            return True
        return False

    @classmethod
    def confirm_recover(cls,recover_token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(recover_token.encode('utf-8'))
        except:
            return None
        
        user = cls.find_by_id(data.get('recover'))
        return user

    @classmethod
    def confirm_account(cls,confirmation_token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(confirmation_token.encode('utf-8'))
        except:
            return False
        
        user = cls.find_by_id(data.get('confirm'))
        if not user:
            return False
        
        user.confirmed = True
        db.session.commit()

        return True

    @classmethod
    def find_by_id(cls,id):
        return User.query.filter_by(id=id).first()

    @classmethod
    def find_by_email(cls,email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_username(cls,username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_session(cls,session_token):
        return cls.query.filter_by(session_token=session_token).first()


    def __repr__(self):
        return f'User<{self.username}>'

class AnonymousUser(AnonymousUserMixin):
    def can(self,perm):
        return False
    
    def is_admin(self):
        return False

login_manager.anonymous_user = AnonymousUser

class Role(db.Model):

    __tablename__ = 'roles'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20),unique=True,nullable=False)
    default = db.Column(db.Boolean,default=False,index=True)
    permissions = db.Column(db.Integer,default=0)

    users = db.relationship('User',backref='role',lazy='dynamic')

    def add_permission(self,perm):
        if not self.has_permission(perm):
            self.permissions+=perm

    def remove_permission(self,perm):
        if self.has_permission(perm):
            self.permissions-=perm

    def reset_permissions(self):
        self.permissions=0

    def has_permission(self,perm):
        return (self.permissions & perm) == perm

    @staticmethod
    def insert_roles():
        roles = {
            'User':[Permission.FOLLOW,Permission.COMMENT,Permission.WRITE],
            'Moderator':[Permission.FOLLOW,Permission.COMMENT,Permission.WRITE,Permission.MODERATE],
            'Administrator':[Permission.FOLLOW,Permission.COMMENT,Permission.WRITE,Permission.MODERATE,Permission.ADMIN]
        }
        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()
    
    def __repr__(self):
        return f'Role<{self.name}>'

class Permission:
    FOLLOW = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16

class Post(db.Model):

    __tablename__ = 'posts'
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(40),nullable=False)
    body = db.Column(db.Text,nullable=False)
    body_html = db.Column(db.Text)
    time_stamp = db.Column(db.DateTime,index=True,default=datetime.utcnow)

    author_id = db.Column(db.Integer,db.ForeignKey('users.id'))

    comments = db.relationship('Comment',backref='post',lazy='dynamic',cascade='delete,delete-orphan')

    @staticmethod
    def on_changed_body(target,value,oldvalue,initiator):
        allowed_tags =['a','abbr','acronym','b','blockquote','code',
                        'em','i','li','ol','pre','strong','ul','h1','h2','h3','p']
        target.body_html = bleach.linkify(
            bleach.clean(
                markdown(value,output_format='html'),
                tags=allowed_tags,
                strip=True
            )
        )  
    
    def to_json(self):
        json_post = {
            'url':url_for('api.get_post',id=self.id),
            'title':self.title,
            'body':self.body,
            'body_html':self.body_html,
            'time_stamp':self.time_stamp,
            'author_url':url_for('api.get_user',id=self.author_id),
            'comments_url':url_for('api.get_post_comments',id=self.id),
            'comments_count':self.comments.count()
        }
        return json_post

    @staticmethod
    def from_json(json_post):
        body = json_post.get('body')
        title = json_post.get('title')
        if body is None or title is None or \
            body == '' or title == '':
            raise ValidationError('post does not have a body or title')
        return Post(title=title,body=body)

    def __repr__(self):
        return f'Post<{self.title}>'

db.event.listen(Post.body,'set',Post.on_changed_body)

class Comment(db.Model):

    __tablename__ = 'comments'
    id = db.Column(db.Integer,primary_key=True)
    body = db.Column(db.Text,nullable=False)
    time_stamp = db.Column(db.DateTime,default=datetime.utcnow,index=True)
    disabled = db.Column(db.Boolean,default=False)

    author_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer,db.ForeignKey('posts.id'))

    def to_json(self):
        json_comment = {
            'url': url_for('api.get_comment', id=self.id),
            'post_url': url_for('api.get_post', id=self.post_id),
            'body': self.body,
            'times_tamp': self.time_stamp,
            'author_url': url_for('api.get_user', id=self.author_id),
        }
        return json_comment

    @staticmethod
    def from_json(json_comment):
        body = json_comment.get('body')
        if body is None or body == '':
            raise ValidationError('comment does not have a body')
        return Comment(body=body)

    def __repr__(self):
        return f'Comment<{self.author_id,self.post_id}>'





