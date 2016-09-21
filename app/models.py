# app/models.py

from app import db


class Users(db.Model):
    id = db.Column(db.Integer, primary_key = TRUE)
    firstname = db.Column(db.String(64), index = TRUE, unique = TRUE)
    lastname = db.Column(db.String(64), index = TRUE, unique = TRUE)
    email = db.Column(db.String, index = TRUE, unique = TRUE)
    password = db.Column(db.String, index = TRUE, unique = TRUE)
    role = db.Column(db.String, index = TRUE, unique = TRUE)



    def __repr__(self):
        return '<Users %r>' % (self.firstname)


class Books(db.Model):
    id = db.Column(db.Integer, primary_key = TRUE)
    title = db.Column(db.String(120), index = TRUE, unique = TRUE)
    author = db.Column(db.String(120), index = TRUE, unique = TRUE)
    isbn = db.Column(db.Integer, index = TRUE, unique = TRUE)
    categoryid = db.Column(db.Integer, index = TRUE, unique = TRUE)
    quantity = db.Column(db.Integer, index = TRUE, unique = TRUE)
    

    def __repr__(self):
        return '<Books %r>' % (self.title)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key = TRUE)
    name = db.Column(db.String(120), index = TRUE, unique = TRUE)
    

    def __repr__(self):
        return '<Category %r>' % (self.name)


class Borrowedbooks(db.Model):
    id = db.Column(db.Integer, primary_key = TRUE)
    bookid = db.Column(db.Integer, index = TRUE, unique = TRUE)
    userid = db.Column(db.Integer, index = TRUE, unique = TRUE)
    status = db.Column(db.Boolean, index = TRUE, unique = TRUE)
    timeborrowed = db.Column(db.DateTime, index = TRUE, unique = TRUE)
    timereturned = db.Column(db.DateTime, index = TRUE, unique = TRUE)
    

    def __repr__(self):
        return '<Books %r>' % (self.bookid)