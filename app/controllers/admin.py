# app/controllers/admin.py

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, logout_user, current_user, login_required, UserMixin
from app import app
from app.forms import EmailPasswordForm, RegistrationForm
from app.models import Users, User, Books, Categories, Borrowedbooks


mod = Blueprint('admin', __name__, template_folder='templates')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin.login'


@login_manager.user_loader
def load_user(user_id):
    user = Users.query.get(int(user_id))
    return user
"""
    The routes are the routes for the front end of the application
    the user with a role == 'user' can view these routes
"""

@mod.route('/')
@mod.route('/index/')
@login_required
def index():
    # user = User(user.id, user.e)
    return render_template('admin/index.html')


@mod.route('/books/')
@login_required
def books():
    books = Books.query.all()
    categories = Categories.query.all()
    return render_template('admin/books.html', books = books, categories = categories)


@mod.route('/login/', methods=['GET', 'POST'])
def login():
    form = EmailPasswordForm()
    if request.method == 'POST' and form.validate():
 
        #Check the email and password in the database and log the user in        
        email = form.email.data
        password = form.password.data
        checkuser = Users.get_user(email = email, password = password)
        if checkuser == None:
            failure = 'Your details are not correct'
            return render_template('admin/login.html', form = form, failure = failure)
        user = User(checkuser.id, checkuser.firstname, checkuser.email)
        login_user(user)
        flash('Logged in Successfully')
        next = request.args.get('index')
        return redirect(next or url_for('admin.index'))
    return render_template('admin/login.html', form = form)




@mod.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for('admin.login'))
