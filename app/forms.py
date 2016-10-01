# ourapp/forms.py

from flask_wtf import Form
from wtforms import StringField, PasswordField, IntegerField, validators
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from models import Categories

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

class BookForm(Form):
    title = StringField('Book Title', [
        validators.Length(min=2, max = 120),
        validators.DataRequired()
    ])
    author = StringField('Author', [
        validators.Length(min = 2, max = 120),
        validators.DataRequired()
    ])
    isbn = StringField('ISBN', [
        validators.Length(min = 6, max = 60), 
        validators.Email(),
        validators.DataRequired()
    ])
    category = QuerySelectField(query_factory=lambda: Categories.query.all(),
        get_label = 'name'
    )

    quantity = IntegerField('Enter the quantity', [
        validators.DataRequired()
    ])

class CategoryForm(Form):
    name = StringField('Category Name', [
        validators.Length(min=2, max = 120),
        validators.DataRequired()
    ])

class UploadForm(Form):
    file = FileField('.', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])