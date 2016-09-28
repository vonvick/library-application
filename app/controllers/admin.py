# app/controllers/admin.py

from flask import Blueprint, render_template, redirect, url_for, request, flash, g, session
from functools import wraps
from flask_login import LoginManager, login_user, logout_user, current_user, login_required, UserMixin
from app import app
from app.forms import EmailPasswordForm, RegistrationForm, BookForm, CategoryForm
from app.models import Users, Books, Categories, Borrowedbooks, User


admin = Blueprint('admin', __name__, url_prefix = '/admin')

@app.before_request
def before_request():
    g.user = current_user

# reroutes all request to the admin page with out the role of admin to the public page
def admin_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user.role != 'admin':
            return redirect(url_for('public.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


"""
    The routes are the routes for the front end of the application
    the user with a role == 'user' can view these routes
"""

@admin.route('/')
@admin.route('/index/')
@login_required
@admin_login
def index():
    user = g.user
    return render_template('admin/index.html', user = user)


@admin.route('/books/')
@login_required
@admin_login
def books():
    user = g.user
    books = Books.query.all()
    categories = Categories.query.all()
    if books == None:
        return render_template('admin/books.html', user = user)
    return render_template('admin/books.html', books = books, categories = categories, user = user)

@admin.route('/addbook/', methods = ['GET', 'POST'])
@login_required
@admin_login
def addbook():
    user = g.user
    form = BookForm()
    if request.method == 'POST' and form.validate:
        title = form.title.data
        author = form.author.data
        isbn = form.isbn.data
        categoryid = request.form.get('category')
        quantity = form.quantity.data
        addbook = Books.create_book(title, author, isbn, categoryid, quantity)
        if addbook == None:
            failure = 'The book already exist'
            return render_template('admin/addbook', form = form, failure = failure, user = user)
        flash('The book has been successfully added')
        return redirect(url_for('admin.books'))
    return render_template('admin/addbook.html', form = form, user = user)


@admin.route('/deletebook/<string:title>', methods = ['GET', 'POST'])
@login_required
@admin_login
def deletebook(title):
    user = g.user
    book = Books.delete_book(title = title)
    flash('The book has been successfully deleted')
    return redirect(url_for('admin.books'))


@admin.route('/editbook/<id>', methods = ['GET', 'POST'])
@login_required
@admin_login
def editbook(id):
    user = g.user
    book = Books.query.get(id)
    categories = Categories.query.all()
    form = BookForm(obj=book)
    if request.method == 'POST':
        book.title = request.form['title']
        book.author = request.form['author']
        book.isbn = request.form['isbn']
        book.categoryid = request.form.get('category')
        book.quantity = request.form['quantity']
        edit = Books.commit()
        return redirect(url_for('admin.books'))
    return render_template('admin/editbook.html', user = user, book = book, categories = categories, form = form)


@admin.route('/categories/')
@login_required
@admin_login
def categories():
    user = g.user
    books = Books.query.all()
    categories = Categories.query.all()
    return render_template('admin/categories.html', books = books, categories = categories, user = user)


@admin.route('/category/create/', methods = ['GET', 'POST'])
@login_required
@admin_login
def createcategory():
    user = g.user
    form = CategoryForm()
    if request.method == 'POST' and form.validate:
        name = form.name.data
        addcategory = Categories.create_category(name)
        if addcategory == None:
            failure = 'The Category already exist'
            return render_template('admin/addcategory.html', form = form, failure = failure, user = user)
        flash('The category has been successfully added')
        return redirect(url_for('admin.categories'))
    return render_template('admin/addcategory.html', form = form, user = user)


@admin.route('/category/edit/<int:id>', methods = ['GET', 'POST'])
@login_required
@admin_login
def editcategory(id):
    user = g.user
    category = Categories.query.get(id)
    form = CategoryForm(obj=category)
    if request.method == 'POST':
        category.name = request.form['name']
        edit = Categories.commit()
        flash('The category has been successfully added')
        return redirect(url_for('admin.books'))
    return render_template('admin/editcategory.html', form = form, user = user, category = category)


@admin.route('/members')
@login_required
@admin_login
def members():
    user = g.user
    members = Users.query.all()
    if members == None:
        return render_template('admin/memberslist.html', members = members, user = user)
    return render_template('admin/memberlist.html', members = members, user = user)


@admin.route('/login/')
def login():
    return redirect(url_for('public.login'))

@admin.route('/logout/')
@login_required
@admin_login
def logout():
    logout_user()
    return redirect(url_for('public.login'))
