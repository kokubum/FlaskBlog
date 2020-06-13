from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField
from wtforms.validators import InputRequired,Email,EqualTo,Regexp,Length

class RegistrationForm(FlaskForm):
    first_name = StringField('First Name',validators=[InputRequired(),Regexp('[A-Z][a-z]*$',message='First name only with uppercase letter')])
    last_name = StringField('Last Name',validators=[InputRequired(),Regexp('[A-Z][a-z]*$',message='Last name only with uppercase letter')])
    email = StringField('Email',validators=[InputRequired(),Email(message='Invalid email address')])
    username = StringField('Username',validators=[InputRequired(),Length(min=5,message='Username must contain at least 5 characters')])
    password = PasswordField(
        'Password',
        validators=[
            InputRequired(),
            Regexp('^(?=.*?[A-Z])(?=.*?[0-9])(?=.*?[@$!%*#?&])$',message="Password must contain at least: Upper case letter, a digit and a special character"),Length(min=8,message="Password must contain at least 8 characters")
        ]
    )
    confirm_password = PasswordField('Confirm Password',validators=[EqualTo('password',message=('Passwords must match'))])

class LoginForm(FlaskForm):
    email = StringField('Email',validators=[InputRequired()])
    password = PasswordField('Password',validators=[InputRequired()])