# app/models.py

from datetime import datetime
from app import db
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug import generate_password_hash, check_password_hash


class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    firstname = db.Column(db.String(64), index = True)
    lastname = db.Column(db.String(64), index = True)
    email = db.Column(db.String(64), index = True, unique = True)
    _password = db.Column(db.String(128))
    role = db.Column(db.String(30), index = True, unique = True)
    userborrowed = db.relationship('Borrowedbooks', backref = 'users', lazy = 'dynamic')

    def __init__(self, firstname, lastname, email, password, role = 'user'):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.set_password(password)
        self.role = role
    
    def set_password(self, password):
        self._password   = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self._password, password)
    # @hybrid_property
    # def password(self):
    #     return self._password

    # @password.setter
    # def _set_password(self, plaintext):
    #     self._password = bcrypt.generate_password_hash(plaintext)

    def __repr__(self):
        return '<Users %r>' % (self.firstname)


class Books(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(120), index = True, unique = True)
    author = db.Column(db.String(120), index = True)
    isbn = db.Column(db.Integer, index = True, unique = True)
    categoryid = db.Column(db.Integer, db.ForeignKey('categories.id'))
    quantity = db.Column(db.Integer, index = True, unique = True)
    bookborrowed = db.relationship('Borrowedbooks', backref = 'books', lazy = 'dynamic')
    
    def __init__(self, title, author, isbn, categoryid, quantity):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.categoryid = categoryid
        self.quantity = quantity

    def __repr__(self):
        return '<Books %r>' % (self.title)


class Categories(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(120), index = True, unique = True)
    books = db.relationship('Books', backref = 'categories', lazy = 'dynamic')
    
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category %r>' % (self.name)


class Borrowedbooks(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    bookid = db.Column(db.Integer, db.ForeignKey('books.id'))
    userid = db.Column(db.Integer, db.ForeignKey('users.id'))
    status = db.Column(db.Boolean)
    timeborrowed = db.Column(db.DateTime)
    timereturned = db.Column(db.DateTime, nullable = True)
    
    def __init__(self, bookid, userid, status, timeborrowed = None):
        self.bookid = bookid
        self.userid = userid
        status = status
        if timeborrowed is None:
            timeborrowed = datetime.utcnow()

    def __repr__(self):
        return '<Books %r>' % (self.bookid)