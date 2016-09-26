# app/models.py

from datetime import datetime
from app import db
from werkzeug import generate_password_hash, check_password_hash
from flask_login import UserMixin


class Users(db.Model):

    __tablename__ = 'users'


    id = db.Column(db.Integer, primary_key = True)
    firstname = db.Column(db.String(64), index = True)
    lastname = db.Column(db.String(64), index = True)
    email = db.Column(db.String(64), index = True, unique = True)
    pwdhash = db.Column(db.String(128), index = True)
    role = db.Column(db.String(30), index = True)
    userborrowed = db.relationship('Borrowedbooks', backref = 'users', cascade='all, delete-orphan', lazy = 'dynamic')

    
    def __init__(self, firstname, lastname, email, password, role = 'user'):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.set_password(password)
        self.role = role
    
    def set_password(self, password):
        self.pwdhash   = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)    

    def __repr__(self):
        return '<Users %r>' % (self.firstname)

    def is_authenticated(self):
        return True
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return unicode(self.id)

    @staticmethod
    def create_user(firstname, lastname, email, password):
        user = Users(
            firstname = firstname, 
            lastname = lastname, 
            email = email, 
            password = password,
            role = 'user'
        )
        checkuser = Users.query.filter_by(email = email).first()
        if checkuser == None:
            db.session.add(user)
            db.session.commit()
            return user
        else:
            return None

    @staticmethod
    def get_user(email, password):
        users = Users.query.filter_by(email = email).first()
        if users == None:
            return None
        if check_password_hash(users.pwdhash, password) == False:
            return None
        return users

    @staticmethod
    def delete_user(email):
        user = Users.query.filter_by(email = email).first()
        if user == None:
            return None
        db.session.delete(user)
        db.session.commit()
        return users

class User(UserMixin):
    def __init__(self, id, firstname, email):
        self.id = id
        self.firstname = firstname
        self.email = email
    
    def is_authenticated(self):
        return True
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return unicode(self.id)

class Books(db.Model):

    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(120), index = True, unique = True)
    author = db.Column(db.String(120), index = True)
    isbn = db.Column(db.String(60), index = True, unique = True)
    categoryid = db.Column(db.Integer, db.ForeignKey('categories.id'))
    quantity = db.Column(db.Integer, index = True)
    bookborrowed = db.relationship('Borrowedbooks', backref = 'books', cascade='all, delete-orphan', lazy = 'dynamic')
    
    def __init__(self, title, author, isbn, categoryid, quantity):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.categoryid = categoryid
        self.quantity = quantity

    def __repr__(self):
        return '<Books %r>' % (self.title)

    @staticmethod
    def get_books():
        books = Books.query.all()
        return books


class Categories(db.Model):

    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(120), index = True, unique = True)
    books = db.relationship('Books', backref = 'categories', cascade='all, delete-orphan', lazy = 'dynamic')
    
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category %r>' % (self.name)


class Borrowedbooks(db.Model):

    __tablename__ = 'borrowedbooks'
    
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