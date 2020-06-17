from wtforms.validators import InputRequired,Email,EqualTo,Regexp,Length,ValidationError
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from flask_wtf import FlaskForm
from ...models import User
import re


class RegistrationForm(FlaskForm):
    first_name = StringField('First Name',validators=[InputRequired(),Regexp('[A-Z][a-z]*$',message='First name only with uppercase letter')])
    last_name = StringField('Last Name',validators=[InputRequired(),Regexp('[A-Z][a-z]*$',message='Last name only with uppercase letter')])
    email = StringField('Email',validators=[InputRequired(),Email(message='Invalid email address')])
    username = StringField('Username',validators=[InputRequired(),Length(min=5,message='Username must contain at least 5 characters')])
    password = PasswordField(
        'Password',
        validators=[
            InputRequired(),
            Regexp('^(?=.*?[A-Z])(?=.*?[0-9])(?=.*?[@$!%*#?&]).*$',message="Password must contain at least: 1 Upper case letter, 1 digit and 1 special character"),Length(min=8,message="Password must contain at least 8 characters")
        ]
    )
    confirm_password = PasswordField('Confirm Password',validators=[EqualTo('password',message=('Passwords must match'))])
    submit = SubmitField('Register')


    def validate_email(self,field):
        user = User.find_by_email(field.data)
        if user:
            raise ValidationError('Email already registered')

    def vaidate_username(self,field):
        user = User.find_by_username(field.data)
        if user:
            raise ValidationError('Username already registered')
    



class LoginForm(FlaskForm):
    email = StringField('Email',validators=[InputRequired()])
    password = PasswordField('Password',validators=[InputRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')