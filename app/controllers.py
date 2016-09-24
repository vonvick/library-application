# app/controllers.py

from flask import render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from app import app
from .forms import EmailPasswordForm, RegistrationForm
from .models import Users, Books, Categories, Borrowedbooks

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@app.route('/')
@app.route('/index/')
@login_required
def index():
    # User's info from database
        
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
        email = form.email.data
        password = form.password.data
        user = Users.get_user(email, password)
        if user is not None:
            login_user(user)
            flash('Logged in Successfully')
            return redirect(request.args.get('next') or url_for('index'))
        return render_template('login.html', form = form)
    return render_template('login.html', form = form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    registerform = RegistrationForm()
    if request.method == 'POST' and registerform.validate():
        user = {'firstname' :registerform.firstname.data,
            'lastname': registerform.lastname.data,
            'email': registerform.email.data,
            'password': registerform.password.data
        }
        # checks the data submitted with format
        flash('Thank you for registering')
        # check if a user with such email already exists, If not
        # insert form data into the database and create a new user
        return redirect(url_for('index'))
    return render_template('signup.html', form = registerform)