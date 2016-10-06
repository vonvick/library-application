# app/models.py

from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from hashlib import md5
from werkzeug import generate_password_hash, check_password_hash

from app import app

db = SQLAlchemy(app)


class Base(db.Model):

    __abstract__ = True

    # saves the data
    @staticmethod
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    # updates the data
    @staticmethod
    def update():
        db.session.commit()

    # deletes the data
    @staticmethod
    def delete(self):
        db.session.add(self)
        db.session.delete(self)
        db.session.commit()

class User(Base, UserMixin):

    __tablename__ = 'user'


    id = db.Column(db.Integer, primary_key = True)
    firstname = db.Column(db.String(64), index = True)
    lastname = db.Column(db.String(64), index = True)
    email = db.Column(db.String(64), index = True, unique = True)
    pwdhash = db.Column(db.String(128), index = True, nullable=True)
    role = db.Column(db.String(30), index = True)
    imagepath = db.Column(db.String(140), index = True)
    provider = db.Column(db.String(128), index = True)
    userborrowed = db.relationship('Borrowedbook', backref = 'users', lazy = 'dynamic')

    
    def __init__(self, firstname, lastname, email, password, role = 'user'):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.set_password(password)
        self.role = role
    
    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)    

    def __repr__(self):
        return '<Users %r>' % (self.firstname)

    def is_authenticated(self):
        return True
 
    def is_active(self):
        return True
 
    def is_anonymous():
        return False

    def get_id(self):
        return unicode(self.id)

    @staticmethod
    def avatar(email, size):
        return 'https://www.gravatar.com/avatar/%s?d=mm&s=%d' %(md5(email.encode('utf-8')).hexdigest(), size)

    @staticmethod
    def create_user(firstname, lastname, email, password):
        user = User(
            firstname =firstname, 
            lastname = lastname, 
            email = email, 
            password = password,
            role = 'user'
        )
        check_user = User.query.filter_by(email = email).first()
        if check_user == None:
            User.save(user)
            return user
        else:
            return None

    @staticmethod
    def get_user(email, password):
        user = User.query.filter(User.email == email).first()
        if user == None:
            return None
        if check_password_hash(user.pwdhash, password) == False:
            return None
        return user

    @staticmethod
    def delete_user(email):
        user = User.query.filter_by(email = email).first()
        if user == None:
            return None
        user.delete()
        return user

    @staticmethod
    def get_all_users():
        users = User.query.all()
        return users


class Book(Base):

    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(120), index = True, unique = True)
    author = db.Column(db.String(120), index = True)
    isbn = db.Column(db.String(60), index = True, unique = True)
    categoryid = db.Column(db.Integer, db.ForeignKey('category.id'))
    quantity = db.Column(db.Integer, index = True)
    description = db.Column(db.String(512))
    status = db.Column(db.String(60), index = True)
    imagepath = db.Column(db.String(140))
    bookborrowed = db.relationship('Borrowedbook', backref = 'books', lazy = 'dynamic')
    
    def __init__(self, title, author, isbn, categoryid, quantity, description, imagepath, status = 'true'):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.categoryid = categoryid
        self.quantity = quantity
        self.description = description
        self.imagepath = imagepath
        self.status = status

    def __repr__(self):
        return '<Books %r>' % (self.title)

    @staticmethod
    def get_books():
        books = Book.query.all()
        return books

    @staticmethod
    def get_book(id):
        book = Book.query.get(id)
        if book == None:
            return None
        return book

    @staticmethod
    def create_book(title, author, isbn, categoryid, quantity, description, imagepath):
        book =  Book(
            title = title, 
            author = author, 
            isbn = isbn, 
            categoryid = categoryid,
            quantity = quantity,
            description = description,
            imagepath = imagepath
        )
        check_book = Book.query.filter_by(title = title).first()
        if check_book == None:
            Book.save(book)
            return book

    @staticmethod
    def delete_book(title):
        book = Book.query.filter_by(title = title).first()
        if book == None:
            return None
        else:
            Book.delete(book)
            return book

    @staticmethod
    def edit_book(id):
        book = Book.query.get(id)
        return book

    @staticmethod
    def get_books_user(userid):
        result = []
        books = Book.query.join(Category, Book.categoryid == Category.id)\
            .order_by(Book.title).all()
        user = User.query.get(userid)
        for book in books:
            not_returned = Borrowedbook.check_borrowed(book, user)
            if not_returned:
                book.status = 'false'
                result.append(book)
            else:
                result.append(book)
        return result


class Category(Base):

    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, unique=True)
    books = db.relationship('Book', backref='category', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category %r>' % (self.name)

    @staticmethod
    def create_category(name):
        category = Category(name)
        check_category = Category.query.filter_by(name=name).first()
        if check_category != None:
            return None
        else:
            Category.save(category)
            return category


class Borrowedbook(Base):

    __tablename__ = 'borrowedbook'

    id = db.Column(db.Integer, primary_key=True)
    bookid = db.Column(db.Integer, db.ForeignKey('book.id'))
    userid = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column(db.String(30), index=True)
    timeborrowed = db.Column(db.DateTime, server_default=db.func.now())
    timereturned = db.Column(db.DateTime, nullable=True)

    def __init__(self, books, users, status='false', timeborrowed=None):
        self.bookid = books.id
        self.userid = users.id
        self.status = status
        if timeborrowed is None:
            self.timeborrowed = datetime.utcnow().replace(microsecond=0)

    def __repr__(self):
        return '<Books %r>' % (self.bookid)

    @staticmethod
    def get_user_history(user):
        history = Borrowedbook.query.join(Book, Borrowedbook.bookid == Book.id)\
            .filter(Borrowedbook.userid == user.id)\
            .order_by(Borrowedbook.timeborrowed)
        return history

    @staticmethod
    def check_borrowed(book, user):
        borrowed_list = Borrowedbook.query\
            .filter(Borrowedbook.userid == user.id)\
            .filter(Borrowedbook.bookid == book.id)\
            .filter(Borrowedbook.status == 'false').first()
        return borrowed_list

    @staticmethod
    def save_borrowed(book, user):
        borrow = Borrowedbook(
            books=book, 
            users=user, 
            status='false', 
            timeborrowed=None
        )
        Borrowedbook.save(borrow)
        return borrow

    @staticmethod
    def return_borrowed(book, user):
        borrowed = Borrowedbook.check_borrowed(book,user)
        if borrowed:
            book.quantity = book.quantity + 1
            book.update()
            borrowed.status = 'true'
            borrowed.timereturned = datetime.utcnow().replace(microsecond=0)
            borrowed.update()
            return borrowed