# app/public/views.py
from flask import Blueprint, current_app, render_template
from . import admin

@admin.route('/')
@admin.route('/index')
def index():
    user = {'nickname': 'Victor'} # User's info from database
    
    return render_template('index.html', user = user)

@admin.route('/books')
def books():
    user = {'nickname': 'Victor'} # User's info from database
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
    return render_template('index.html', user = user, books = books)