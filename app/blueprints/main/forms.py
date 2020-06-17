from wtforms import StringField,TextAreaField,SubmitField,BooleanField,SelectField
from wtforms.validators import Length,Regexp,InputRequired,Email
from flask_wtf import FlaskForm
from app.models import Role,User

class EditProfileForm(FlaskForm):
    first_name = StringField('First Name',validators=[InputRequired(),Regexp('[A-Z][a-z]*$',message='First name only with uppercase letter')])
    last_name = StringField('Last Name',validators=[InputRequired(),Regexp('[A-Z][a-z]*$',message='Last name only with uppercase letter')])
    location = StringField('Location',validators=[Length(0,64)])
    about_me = TextAreaField('About Me')

    submit = SubmitField('Edit')

class EditProfileAdminForm(FlaskForm):
    email = StringField('Email',validators=[InputRequired(),Email(message='Invalid email address')])
    username = StringField('Username',validators=[InputRequired(),Length(min=5,message='Username must contain at least 5 characters')])
    confirmed = BooleanField('Confirmed')
    role = SelectField('Role',coerce=int)
    first_name = StringField('First Name',validators=[InputRequired(),Regexp('[A-Z][a-z]*$',message='First name only with uppercase letter')])
    last_name = StringField('Last Name',validators=[InputRequired(),Regexp('[A-Z][a-z]*$',message='Last name only with uppercase letter')])
    location = StringField('Location',validators=[Length(0,64)])
    about_me = TextAreaField('About Me')

    submit = SubmitField('Edit')

    def __init__(self,user,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.role.choices = [(role.id,role.name) for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self,field):
        user = User.find_by_email(field.data)
        if field.data!=self.user.email and user:
            raise ValidationError('Email already registered')

    def validate_username(self,field):
        user = User.find_by_username(field.data)
        if field.data!=self.user.username and user:
            raise ValidationError('Username already registered')

class PostForm(FlaskForm):
    title = StringField('Title',validators=[InputRequired()])
    body = TextAreaField('Content',validators=[InputRequired()])
    submit = SubmitField('Post')