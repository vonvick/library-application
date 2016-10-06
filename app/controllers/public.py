# app/controllers/public.py

from flask import Blueprint, render_template, redirect, url_for, request, flash, g, jsonify, json
from flask_login import LoginManager, login_user, logout_user, current_user, login_required, UserMixin
from flask_sqlalchemy import SQLAlchemy

from cloudinary.uploader import upload
from cloudinary.api import delete_resources
from cloudinary.utils import cloudinary_url

from app import app
from app.forms import EmailPasswordForm, RegistrationForm, UploadForm
from app.models import User, Book, Category, Borrowedbook

public = Blueprint('public', __name__)

@app.before_request
def before_request():
    g.user = current_user


@public.route('/')
def index():
    user = g.user
    return render_template('public/index.html', user=user)


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

        save_user = User.create_user(firstname, lastname, email, password)
        if save_user == None: 
            failure = 'This email address already exists in our register. \
            Please enter another one  or go to the login page to login.'
            return render_template('public/signup.html', form=registerform, failure=failure)
        
        #redirects to the dashboard page after successful RegistrationForm
        flash('You have been successfully registered')
        user = save_user
        login_user(user)
        return redirect(url_for('public.dashboard')) 
    return render_template('public/signup.html', form=registerform)


@public.route('/login/', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('public.dashboard'))
    form = EmailPasswordForm()
    if request.method == 'POST' and form.validate():
        #Check the email and password in the database and log the user in        
        email = form.email.data
        password = form.password.data
        is_user = User.get_user(email, password)
        if is_user == None:
            failure = 'Your details are not correct'
            return render_template('public/login.html', form=form, failure=failure)
        user = is_user
        login_user(user)
        flash('Logged in Successfully')
        if user.role == 'admin':
            return redirect(url_for('admin.index'))
        return redirect(url_for('public.dashboard'))
    return render_template('public/login.html', form=form, user=g.user)


@public.route('/social/login', methods=['POST'])
def social_login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('public.dashboard'))
    if request.method == 'POST':
        json_dict = request.get_json()

        email = json_dict['email']
        firstname = json_dict['name'].split(' ')[0]
        lastname = json_dict['name'].split(' ')[-1]
        password = json_dict['id']
        save_user = User.create_user(firstname, lastname, email, password)
        if save_user == None:
            is_user = User.get_user(email, password)
            if is_user:
                login_user(is_user)
                success = 'You have successfully logged-in'
                data = {
                    'status': str(success),
                }
                return jsonify(data)
        login_user(save_user)
        success = 'You have successfully logged-in'
        data = {
            'status': str(success),
        }
        return jsonify(data)

    

@public.route('/profile/', methods=['GET', 'POST'])
@login_required
def profile():
    user = g.user
    person = User.query.get(user.id)
    form = RegistrationForm(obj=user)
    if request.method == 'POST':
        person.firstname = request.form['firstname']
        person.lastname = request.form['lastname']
        User.update()
        return redirect(url_for('public.dashboard'))
    return render_template('public/profile.html', person=person, user=user, form=form)

    
@public.route('/profile/upload', methods=['GET', 'POST'])
@login_required
def uploadpic():
    user = g.user
    form  = UploadForm()
    person = User.query.get(user.id)
    if request.method == 'POST':
        file = request.files['file']
        if file:
            upload_result = upload(file)
            old_url = person.imagepath
            imageurl = upload_result['url']
            if old_url is None:
                person.imagepath = imageurl
                User.update()
            else:
                old_image_name = old_url.split('/')[-1].split('.')[0]
                delete_old_image = delete_resources([old_image_name])
                person.imagepath = imageurl
                User.update()
            return redirect(url_for('public.profile'))
    return render_template('public/picture_upload.html', user=user, form=form)



@public.route('/dashboard/')
@login_required
def dashboard():
    user = g.user
    user_borrowed = Borrowedbook.get_user_history(user)
    if user_borrowed: 
        return render_template('public/dashboard.html', user=user, books=books,
            user_borrowed = user_borrowed)
    else:
        message = 'You do not have any books in your custody'
        data = {'status': str(message)}
        return jsonify(data)
    return render_template('public/dashboard.html', user=user, message=message)


@public.route('/books/')
@login_required
def books():
    user = g.user
    books = Book.get_books_user(user.id)
    return render_template('public/books.html', books=books,\
        user=user)


@public.route('/borrowbook/<int:id>')
@login_required
def borrow(id):
    user = g.user
    book = Book.get_book(id)
    not_returned = Borrowedbook.check_borrowed(user, book)
    if book.quantity > 0:
        if not_returned:
            failure = 'Sorry, you can not borrow this book as you '\
                'have not returned this book you collected before' 
            data = {
                'status': str(success),
                'quantity': str(book.quantity)
            }
            return jsonify(data)
        borrow_book = Borrowedbook.save_borrowed(book, user)
        book.quantity = book.quantity - 1
        book.update()
        success = 'You have succesfully borrowed this book'
        data = {
            'status': str(success),
            'quantity': str(book.quantity)
            }
        return jsonify(data)
    failure ='Sorry the book is no longer available'
    data = {'status': str(failure)}
    return jsonify(data) 


@public.route('/returnbook/<int:id>')
@login_required
def replace(id):
    user = g.user
    book = Book.get_book(id)

    ''' 
        checks if a borrowed book returned status is false 
        then sets it to true and increase the quantity by 1
    '''
    returned = Borrowedbook.return_borrowed(book, user)
    if returned:
        success = 'You have returned this book'
        quantity = Book.query.get(id).quantity
        data = {
            'status': str(success),
            'quantity': str(quantity)
        }
        return jsonify(data)
    failure = 'Your book could not be returned'
    quantity = Book.query.get(title).quantity
    data = {
        'status': str(failure),
        'quantity': str(quantity)
    }
    return jsonify(data)

@public.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('public.login'))