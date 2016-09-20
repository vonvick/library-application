# app/public/views.py
from flask import Blueprint, current_app, render_template
from . import admin

@admin.route('/')
@admin.route('/index')
def index():
    user = {'nickname': 'Victor'} # User's info from database
    
    return render_template('index.html', user = user)