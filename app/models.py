from app import db, bcrypt


class User(db.Model):

    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),nullable=False) 
    email = db.Column(db.String(40),unique=True,nullable=False,index=True)
    username = db.Column(db.String(40),unique=True,nullable=False,index=True)
    password_hash = db.Column(db.String(64),nullable=False)

    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))

    @property
    def password():
        raise AttributeError("You can't acess the password")

    @password.setter
    def password(self,password):
        self.password_hash = bcrypt.generate_password_hash(password)

    def check_password(self,password):
        return bcrypt.check_password_hash(self.password_hash,password)

class Role(db.Model):

    __tablename__ = 'roles'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20),unique=True,nullable=False)

    users = db.relationship('User',backref='role',lazy='dynamic')


