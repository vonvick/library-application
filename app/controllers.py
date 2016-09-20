# app/controllers.py

from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Victor'} # User's info from database
    
    return render_template('index.html', user = user)

@app.route('/books')
def books():
    books = [  # To be gotten from the database
        { 
            'author': {'nickname': 'John'}, 
            'title': 'Things fall apart',
            'amount': 10 
        },
        { 
            'author': {'nickname': 'Susan'}, 
            'title': 'The Avengers',
            'amount': 10
        },
        { 
            'author': {'nickname': 'Wole'}, 
            'title': 'The lion and the Jewel',
            'amount': 10
        }
    ]
    return render_template('books.html', books = books)

@app.route('/login')
def login():
    return render_template('login.html')