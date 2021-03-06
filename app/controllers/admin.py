# app/controllers/admin.py

from flask import Blueprint, render_template, redirect, url_for, request, flash, g, session
from flask_login import LoginManager, login_user, logout_user, current_user, login_required, UserMixin
from functools import wraps

from cloudinary.uploader import upload
from cloudinary.api import delete_resources
from cloudinary.utils import cloudinary_url

from app import app
from app.forms import EmailPasswordForm, RegistrationForm, BookForm, CategoryForm
from app.models import User, Book, Category, Borrowedbook


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
@login_required
@admin_login
def index():
    user = g.user
    borrowed = Borrowedbook.query\
        .join(Book, Borrowedbook.bookid == Book.id)\
        .join(User, Borrowedbook.userid == User.id)\
        .filter(Borrowedbook.status == 'false').all()
    if borrowed is None:
        message = 'All books have been returned'
    return render_template('admin/index.html', user=user, borrowed=borrowed)

@admin.route('/books/')
@login_required
@admin_login
def books():
    user = g.user
    books = Book.query.join(Category, Book.categoryid == Category.id).all()
    if books == None:
        return render_template('admin/books.html', user=user)
    return render_template('admin/books.html', books=books, user=user)

@admin.route('/addbook/', methods=['GET', 'POST'])
@login_required
@admin_login
def addbook():
    user = g.user
    form = BookForm()
    if request.method == 'POST' and form.validate():
        title = form.title.data
        author = form.author.data
        isbn = form.isbn.data
        category_id = request.form.get('category')
        description = form.description.data
        quantity = form.quantity.data
        file = request.files['file']
        if file:
            upload_result = upload(file)
            imageurl, options = cloudinary_url(upload_result['public_id'], 
                format = 'jpg', width=250, height=250, crop='fit')
        add_book = Book.create_book(title, author, isbn, category_id, quantity,
            description, imageurl)
        if add_book == None:
            flash('The book already exist')
            return render_template('admin/addbook', form=form, user=user)
        flash('The book has been successfully added')
        return redirect(url_for('admin.books'))
    return render_template('admin/addbook.html', form=form, user=user)


@admin.route('/editbook/<id>', methods=['GET', 'POST'])
@login_required
@admin_login
def editbook(id):
    user = g.user
    book = Book.edit_book(id)
    categories = Category.query.all()
    old_image = book.imagepath
    form = BookForm(obj=book)
    if request.method == 'POST' and form.validate():
        book.title = request.form['title']
        book.author = request.form['author']
        book.isbn = request.form['isbn']
        book.categoryid = request.form.get('category')
        book.quantity = request.form['quantity']
        book.description = request.form['description']
        book.imagepath = request.files['file']
        if book.imagepath:
            upload_result = upload(book.imagepath)
            old_url = old_image
            imageurl, options = cloudinary_url(upload_result['public_id'], 
                format='jpg', width=250, height=250, crop='fit')
            if old_url is None:
                book.imagepath = imageurl
            else:
                old_image_name = old_url.split('/')[-1].split('.')[0]
                delete_old_image = delete_resources([old_image_name])
                book.imagepath = imageurl
        Book.update()
        return redirect(url_for('admin.books'))
    return render_template('admin/editbook.html', user=user, book=book, categories=categories, form=form)


@admin.route('/deletebook/<string:title>', methods=['GET', 'POST'])
@login_required
@admin_login
def deletebook(title):
    user = g.user
    book = Book.delete_book(title=title)
    flash('The book has been successfully deleted')
    return redirect(url_for('admin.books'))


@admin.route('/categories/')
@login_required
@admin_login
def categories():
    user = g.user
    books = Book.query.all()
    categories = Category.query.all()
    return render_template('admin/categories.html', books=books, categories=categories, user=user)


@admin.route('/category/create/', methods=['GET', 'POST'])
@login_required
@admin_login
def createcategory():
    user = g.user
    form = CategoryForm()
    if request.method == 'POST' and form.validate():
        name = form.name.data
        add_category = Category.create_category(name)
        if add_category == None:
            failure = 'The Category already exist'
            return render_template('admin/addcategory.html', form=form, failure=failure, user=user)
        flash('The category has been successfully added')
        return redirect(url_for('admin.categories'))
    return render_template('admin/addcategory.html', form=form, user=user)


@admin.route('/category/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_login
def editcategory(id):
    user = g.user
    category = Category.query.get(id)
    form = CategoryForm(obj=category)
    if request.method == 'POST' and form.validate():
        category.name = request.form['name']
        edit = category.update()
        flash('The category has been successfully added')
        return redirect(url_for('admin.categories'))
    return render_template('admin/editcategory.html', form=form, user=user, category=category)


@admin.route('/members')
@login_required
@admin_login
def members():
    user = g.user
    members = User.query.all()
    if members == None:
        return render_template('admin/memberslist.html', members=members, user=user)
    return render_template('admin/memberlist.html', members=members, user=user)


@admin.route('/login/')
def login():
    return redirect(url_for('public.login'))

@admin.route('/logout/')
@login_required
@admin_login
def logout():
    logout_user()
    return redirect(url_for('public.login'))
