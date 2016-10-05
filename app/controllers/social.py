# app/controllers/social.py

from flask import Blueprint, render_template, redirect, url_for, request, flash, g, jsonify
from flask_login import LoginManager, login_user, logout_user, current_user, login_required, UserMixin
from flask_sqlalchemy import SQLAlchemy

from app import app
from app.models import User, Book, Category, Borrowedbook

social = Blueprint('social', __name__, url_prefix = '/social')

@social.route('/')
def index():
    user = g.user
    return render_template('public/index.html', user = user)
