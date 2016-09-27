# app/controllers/public.py

from flask import Blueprint, render_template, redirect, url_for, request, flash, g, session
from flask_login import LoginManager, login_user, logout_user, current_user, login_required, UserMixin
from app import app
from app.forms import EmailPasswordForm, RegistrationForm
from app.models import Users, Books, Categories, Borrowedbooks, User


public = Blueprint('public', __name__)

@app.before_request
def before_request():
    g.user = current_user
"""
    The routes are the routes for the front end of the application
    the user with a role == 'user' can view these routes
"""

@public.route('/')
@public.route('/index/')
def index():
    # user = User(user.id, user.e)
    return render_template('public/index.html')


@public.route('/books/')
@login_required
def books():
    books = Books.query.all()
    categories = Categories.query.all()
    return render_template('public/books.html', books = books, categories = categories)


@public.route('/login/', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('public.index'))
    form = EmailPasswordForm()
    if request.method == 'POST' and form.validate():
 
        #Check the email and password in the database and log the user in        
        email = form.email.data
        password = form.password.data
        checkuser = Users.get_user(email = email, password = password)
        if checkuser == None:
            failure = 'Your details are not correct'
            return render_template('public/login.html', form = form, failure = failure) 
        user = User(checkuser.id, checkuser.firstname, checkuser.email, checkuser.role)
        login_user(user)
        flash('Logged in Successfully')
        next = request.args.get('index')
        if user.role == 'admin':
            return redirect(next or url_for('admin.index'))
        return redirect(next or url_for('public.index'))
    return render_template('public/login.html', form = form)


@public.route('/register/', methods=['GET', 'POST'])
def register():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('public.index'))
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
            return render_template('public/signup.html', form = registerform, failure = failure)
        flash('You have been successfully registered')
        user = User(save_user.id, save_user.firstname, save_user.email, save_user.role)
        login_user(user)
        return redirect(url_for('public.index')) 
    return render_template('public/signup.html', form = registerform)


@public.route('/borrowbook/<string:title>')
@login_required
def borrow(title):
    book = Books.get_book(title)
    if book:
        borrowbook = 

@public.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('public.login'))


@public.route('/admin/login')
def admin_login():
    return redirect(url_for('admin.login'))