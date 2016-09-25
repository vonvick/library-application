# app/controllers.py

from flask import render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, logout_user, current_user, login_required, UserMixin
from app import app
from .forms import EmailPasswordForm, RegistrationForm
from .models import Users, User, Books, Categories, Borrowedbooks

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    user = Users.query.get(int(user_id))
    return user
"""
    The routes are the routes for the front end of the application
    the user with a role == 'user' can view these routes
"""

@app.route('/')
@app.route('/index/')
@login_required
def index():
    # user = User(user.id, user.e)
    return render_template('index.html')


@app.route('/books')
@login_required
def books():
    books = Books.query.all()
    categories = Categories.query.all()
    return render_template('books.html', books = books, categories = categories)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = EmailPasswordForm()
    if request.method == 'POST' and form.validate():
 
        #Check the email and password in the database and log the user in        
        email = form.email.data
        password = form.password.data
        checkuser = Users.get_user(email = email, password = password)
        if checkuser == None:
            failure = 'Your details are not correct'
            return render_template('login.html', form = form, failure = failure)
        user = User(checkuser.id, checkuser.firstname, checkuser.email)
        login_user(user)
        flash('Logged in Successfully')
        next = request.args.get('index')
        return redirect(next or url_for('index'))
    return render_template('login.html', form = form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    registerform = RegistrationForm()
    if request.method == 'POST' and registerform.validate():
        firstname = registerform.firstname.data
        lastname =  registerform.lastname.data
        email = registerform.email.data
        password = registerform.password.data

        save_user = Users.create_user(firstname, lastname, email, password)
        if save_user == None:
            failure = 'This email address already exists in our register. \
            Please enter another one  or go to the login page to login.'
            return render_template('signup.html', form = registerform, failure = failure)
        flash('You have been successfully registered')
        return redirect(url_for('index')) 
    return render_template('signup.html', form = registerform)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


"""
    The routes with "/admin" is for the admin part of the site. 
    Only users with admin privileges can view or access these pages
"""

@app.route('/admin')
@app.route('/admin/index')
@login_required
def admin_index():
    # user = User(user.id, user.e)
    return render_template('index.html')


@app.route('admin/books')
@login_required
def books():
    books = Books.query.all()
    categories = Categories.query.all()
    return render_template('books.html', books = books, categories = categories)

