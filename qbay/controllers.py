from flask import (render_template, request, session,
                    redirect, Flask, flash)
                    # url_for)
from flask_login import LoginManager
from qbay.models import (login, register, update, User,
                        createListing, updateListing, Listing)

from datetime import date, datetime

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Length

from qbay import app


# Create Authentication
def authenticate(inner_function):
    """
    :param inner_function: any python function that accepts a user object
    Wrap any python function and check the current session to see if 
    the user has logged in. If login, it will call the inner_function
    with the logged in user object.
    To wrap a function, we can put a decoration on that function.
    Example:
    @authenticate
    def home_page(user):
        pass
    """

    def wrapped_inner():

        # check did we store the key in the session
        if 'logged_in' in session:
            email = session['logged_in']
            try:
                user = User.query.filter_by(email=email).one_or_none()
                if user:
                    # if the user exists, call the inner_function
                    # with user as parameter
                    return inner_function(user)
            except Exception:
                pass
        else:
            # else, redirect to the login page
            return redirect('/login')

    # return the wrapped version of the inner_function:
    return wrapped_inner


# Create Login Form
class LoginForm(FlaskForm):
    email = StringField("Email", validators = [DataRequired()])
    password = PasswordField("Password", validators = [DataRequired()])
    submit = SubmitField("Submit")


# Create Login Page
# GET - requesting data from a specific source
@app.route('/login', methods=['GET'])
def login_get():
    # return back to the login template
    return render_template('login.html', message='Enter your email and password')


# POST - sending data to a server to create/update a resource
@app.route('/login', methods=['POST'])
def login_post():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        errorMsgFlash = None

        session['email'] = email
        session['password'] = password
        success = login(email, password)
        if not success:
            errorMsgFlash = "Login failed. Please try again."
            if errorMsgFlash:
                return render_template("login.html", message=errorMsgFlash)
            return redirect('/login')
        return redirect('/dashboard')


# Create Dashboard Page
@app.route('/dashboard', methods=['GET'])
def dashboard_get():
    return render_template('dashboard.html', message='Successful Login')


# LOGOUT
@app.route('/logout')
def logout():
    session["name"] = None
    if 'logged_in' in session:
        session.pop('logged_in', None)
    return redirect('/')


# Flask_Login Codes
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


