# app/models.py

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5
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

class Users(Base):

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
    def avatar(email, size):
        return 'http://www.gravatar.com/avatar/%s?d=mm&s=%d' %(md5(email.encode('utf-8')).hexdigest(), size)




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
            Users.save(user)
            return user
        else:
            return None

    @staticmethod
    def get_user(email, password):
        user = Users.query.filter_by(email = email).first()
        if user == None:
            return None
        if check_password_hash(user.pwdhash, password) == False:
            return None
        return user

    @staticmethod
    def delete_user(email):
        user = Users.query.filter_by(email = email).first()
        if user == None:
            return None
        user.delete()
        return users

    @staticmethod
    def get_all_users():
        users = Users.query.all()
        return users

class User(UserMixin):
    def __init__(self, id, firstname, email, role):
        self.id = id
        self.firstname = firstname
        self.email = email
        self.role = role
    
    def is_authenticated(self):
        return True
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return unicode(self.id)

    def avatar(self, size):
        return 'http://www.gravatar.com/avatar/%s?d=mm&s=%d' %(md5(self.email.encode('utf-8')).hexdigest(), size)

class Books(Base):

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

    @staticmethod
    def get_book(title):
        book = Books.query.filter_by(title = title).first()
        if book == None:
            return None
        return book

    @staticmethod
    def create_book(title, author, isbn, categoryid, quantity):
        book =  Books(
            title = title, 
            author = author, 
            isbn = isbn, 
            categoryid = categoryid,
            quantity = quantity
        )
        checkbook = Books.query.filter_by(title = title).first()
        if checkbook == None:
            Books.save(book)
            return book

    @staticmethod
    def delete_book(title):
        book = Books.query.filter_by(title = title).first()
        if book == None:
            return None
        else:
            Books.delete(book)
            return book

    @staticmethod
    def edit_book(title, author, isbn, categoryid, quantity):
        
        book = Books.query.filter_by(title = title).first()
        book.title = title
        book.author = author
        book.isbn = isbn
        book.categoryid = categoryid
        book.quantity = quantity
        book.update()
        return book


class Categories(Base):

    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(120), index = True, unique = True)
    books = db.relationship('Books', backref = 'categories', cascade='all, delete-orphan', lazy = 'dynamic')
    
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category %r>' % (self.name)

    @staticmethod
    def create_category(name):
        category = Categories(name)
        checkcategory = Categories.query.filter_by(name = name).first()
        if checkcategory != None:
            return None
        else:
            Categories.save(category)
            return category


class Borrowedbooks(Base):

    __tablename__ = 'borrowedbooks'
    
    id = db.Column(db.Integer, primary_key = True)
    bookid = db.Column(db.Integer, db.ForeignKey('books.id'))
    userid = db.Column(db.Integer, db.ForeignKey('users.id'))
    status = db.Column(db.String(30), index = True)
    timeborrowed = db.Column(db.DateTime, server_default = db.func.now())
    timereturned = db.Column(db.DateTime, nullable = True)
    
    def __init__(self, books, users, status = 'false', timeborrowed = None):
        self.bookid = books.id
        self.userid = users.id
        self.status = status
        if timeborrowed is None:
            self.timeborrowed = datetime.utcnow().replace(microsecond = 0)

    def __repr__(self):
        return '<Books %r>' % (self.bookid)

    @staticmethod
    def checkborrowed(book, user):
        borrowedlist = Borrowedbooks.query.filter(Borrowedbooks.status == 'false' and \
            Borrowedbooks.userid == user.id and \
            Borrowedbooks.bookid == book.id).first()
        if borrowedlist:
            return borrowedlist

    @staticmethod
    def saveborrowed(book, user):
        borrow = Borrowedbooks(
            books = book, 
            users = user, 
            status = 'false', 
            timeborrowed = None
        )
        Borrowedbooks.save(borrow)
        return borrow

    @staticmethod
    def returnborrowed(book, user):
        borrowed = Borrowedbooks.checkborrowed(book,user)
        if borrowed:
            book.quantity = book.quantity + 1
            book.update()
            borrowed.status = 'true'
            borrowed.timereturned = datetime.utcnow().replace(microsecond = 0)
            borrowed.update()
            return borrowed