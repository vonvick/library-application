# app/controllers.py

from flask import render_template, redirect, url_for
from app import app
from .forms import EmailPasswordForm


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

@app.route('/login', methods=["GET", "POST"])
def login():
    form = EmailPasswordForm()
    if form.validate_on_submit():

        # Check the password and log the user in
        

        return redirect(url_for('index'))
    return render_template('login.html', form=form)