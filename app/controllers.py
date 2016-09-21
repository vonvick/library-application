# app/controllers.py

from flask import render_template, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from app import app
from .forms import EmailPasswordForm, RegistrationForm


@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Victor'} # User's info from database
    
    return render_template('index.html', user = user)

@app.route('/books')
def books():
    books = [  # To be gotten from the database
        { 
            'author': {'nickname': 'John'}, 
            'title': 'Things fall apart',
            'amount': 10 
        },
        { 
            'author': {'nickname': 'Susan'}, 
            'title': 'The Avengers',
            'amount': 10
        },
        { 
            'author': {'nickname': 'Wole'}, 
            'title': 'The lion and the Jewel',
            'amount': 10
        }
    ]
    return render_template('books.html', books = books)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = EmailPasswordForm()
    if request.method == 'POST' and form.validate():
        # Check the password and log the user in
        if form.email.data == 'vonvikky@gmail.com' and form.password.data == 'olusegun':
            return redirect(url_for('index'))
        return render_template('login.html', form = form)
    return render_template('login.html', form = form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    registerform = RegistrationForm()
    if request.method == 'POST' and registerform.validate():
        user = User(registerform.firstname.data, registerform.lastname.data, registerform.email.data,
                    form.password.data)
        # checks the data submitted with format
        flash('Thank you for registering', user.firstname)
        # check if a user with such email already exists, If not
        # insert form data into the database and create a new user
        return redirect(url_for('index'))
    return render_template('signup.html', form = registerform)