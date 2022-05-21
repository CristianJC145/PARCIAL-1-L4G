from unicodedata import numeric
from wsgiref.validate import validator
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email

"""class RegistrationForm(FlaskForm):
    username = StringField('username' , 
                        validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('email' , 
                        validators=[DataRequired(), Email()])
    password = StringField('password', validators=[DataRequired()])
    confirm_password = PasswordField('confirm_password',
                                    validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')"""


class LoginForm(FlaskForm):
    email = StringField('Email' , 
                        validators=[DataRequired(), Email()], id="email")
    password = PasswordField('Password', validators=[DataRequired()], id="password")

class EditUser(FlaskForm):
    name = StringField('Name', id="name")
    phone = StringField('Phone', id="phone")
    address = StringField('Address', id="address")
    description = StringField('Description', id="description")
    
    submit = SubmitField('Save')