# ourapp/forms.py

from flask_wtf import Form
from wtforms import StringField, PasswordField, validators
# from wtforms.validators import DataRequired, Email

class EmailPasswordForm(Form):
    email = StringField('Email', [
        validators.DataRequired(),
        validators.Email()
    ])
    password = PasswordField('Password', [
        validators.DataRequired()
    ])

class RegistrationForm(Form):
    firstname = StringField('First Name', [validators.Length(min=2, max = 30)])
    lastname =StringField('Last Name', [validators.Length(min = 2, max = 30)])
    email = StringField('Email Address', [
        validators.Length(min = 6, max = 35), 
        validators.Email(),
        validators.DataRequired()
    ])
    password = PasswordField('Enter Your Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')