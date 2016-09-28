# app/controllers/public.py

from flask import Blueprint, render_template, redirect, url_for, request, flash, g, session
from flask_login import LoginManager, login_user, logout_user, current_user, login_required, UserMixin
from app import app
from app.forms import EmailPasswordForm, RegistrationForm
from app.models import Users, Books, Categories, Borrowedbooks, User

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

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
    user = g.user
    return render_template('public/index.html', user = user)


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
        
        #redirects to the dashboard page after successful RegistrationForm
        flash('You have been successfully registered')
        user = User(save_user.id, save_user.firstname, save_user.email, save_user.role)
        login_user(user)
        return redirect(url_for('public.dashboard')) 
    return render_template('public/signup.html', form = registerform)


@public.route('/login/', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('public.dashboard'))
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
        return redirect(next or url_for('public.dashboard'))
    return render_template('public/login.html', form = form, user = g.user)


@public.route('/dashboard/')
@login_required
def dashboard():
    user = g.user
    books = Books.query.all()
    categories = Categories.query.all()
    userborrowed = Borrowedbooks.query.filter_by(userid = user.id).\
        order_by(Borrowedbooks.timeborrowed)
    if userborrowed is not None: 
        return render_template('public/dashboard.html', user = user, books = books, userborrowed = userborrowed, categories = categories)
    message = 'You do not have any books in your custody'
    return render_template('public/dashboard.html', user = user, message = message)

@public.route('/books/')
@login_required
def books():
    user = g.user
    books = Books.query.all()
    categories = Categories.query.all()
    return render_template('public/books.html', books = books, categories = categories, user = user)


@public.route('/borrowbook/<string:title>')
@login_required
def borrow(title):
    user = g.user
    book = Books.get_book(title)
    if book.quantity > 0:
        borrowbook = Borrowedbooks.saveborrow(bookid = book.id, userid = user.id)
        book.quantity = book.quantity - 1
        edit = Books.commit()
        success = 'You have borrowed this book'
        return redirect(url_for('public.books', success = success))
    else:
        failure ='Sorry the book is no longer available'
        return render_template('public/books.html', failure = failure, user = user)
    return render_template('public/books.html', user = user)


@public.route('/returnbook/<string:title>')
@login_required
def replace(title):
    user = g.user
    book = Books.get_book(title)
    borrowed = Borrowedbooks.check_borrowed(book.id, user.id, status = 'false')
    if borrowed != None:
        book.quantity = book.quantity + 1
        borrowed.status = 'true'
        save = Borrowedbooks.commit()
        success = 'You have returned this book'
        return redirect(url_for('public.books', success = success))
    else:
        failure ='Sorry, you did not borrow this book'
        return render_template('public/books.html', failure = failure, user = user)
    return render_template('public/books.html', user = user)

@public.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('public.login'))


@public.route('/admin/login')
def admin_login():
    return redirect(url_for('admin.login'))