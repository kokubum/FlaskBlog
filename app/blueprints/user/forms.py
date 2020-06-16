from wtforms import StringField,TextAreaField,SubmitField
from wtforms.validators import Length,Regexp
from flask_wtf import FlaskForm

class EditProfileForm(FlaskForm):
    first_name = StringField('First Name',validators=[Regexp('[A-Z][a-z]*$',message='First name only with uppercase letter')])
    last_name = StringField('Last Name',validators=[Regexp('[A-Z][a-z]*$',message='Last name only with uppercase letter')])
    location = StringField('Location',validators=[Length(0,64)])
    about_me = TextAreaField('About Me')

    submit = SubmitField('Edit')