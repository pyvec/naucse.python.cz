## Final Assignment

Your task is to create simple web application which will track your sport activity.

### Assignment steps

1. Create GitHub repository for your project
2. Install locally on your laptop Flask
{% filter solution %}
```bash
python -m venv venv
source venv/bin/activate
pip install flask
```
{% endfilter %}
3. Create project structure for Flask application

{% filter solution %}
```bash
|-activity
  |-app/
    |-templates/
    |-static/
    |-main/
      |-__init__.py
      |-errors.py
      |-forms.py
      |-views.py
    |-__init__.py
    |-email.py
    |-models.py
  |-migrations/
  |-tests/
    |-__init__.py
    |-test*.py
  |-venv/
  |-requirements.txt
  |-config.py
  |-activity.py


mkdir {app,migrations,tests}
mkdir app/{templates,static,main}
touch requirements.txt
touch config.py
touch activity.py
touch app/__init__.py
touch app/main/__init__.py
```
{% endfilter %}

Content of config.py

{% filter solution %}
```python
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', '587'))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in \
        ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ACTIVITY_MAIL_SUBJECT_PREFIX = '[Activity]'
    ACTIVITY_MAIL_SENDER = 'Activity Admin <activity@example.com>'
    ACTIVITY_ADMIN = os.environ.get('ACTIVITY_ADMIN')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite://'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
```
{% endfilter %}

4. Integrate Travis CI/CD with your GitHub project

Content of .travis.yml

{% filter solution %}

```bash
dist: xenial   # required for Python >= 3.7
language: python
python:
  - "3.7"
# command to install dependencies
install:
  - pip install -r requirements.txt
# command to run tests
script:
  - pytest

```
{% endfilter %}

Content of tests/test_math.py:

{% filter solution %}

```bash
import math

def test_sqrt():
   num = 25
   assert math.sqrt(num) == 5
```
{% endfilter %}


Content of app/\_\_init\_\_.py:

{% filter solution %}
```python
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)

    # attach routes and custom error pages here

    return app
```
{% endfilter %}


Content of activity.py

{% filter solution %}
```python
import os
import click
from flask_migrate import Migrate
from app import create_app, db

@pytest.fixture
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)

@app.shell_context_processor
def make_shell_context():
    return dict(db=db)

@app.route('/')
def hello():
    return "Hello World!"
```
{% endfilter %}


Content of app/models.py

{% filter solution %}
from werkzeug.security import generate_password_hash, check_password_hash
from . import db


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username

{% endfilter %}


Content of test/test_user_model.py:

{% filter solution %}
import unittest
from app.models import User

class UserModelTestCase(unittest.TestCase):
    def test_password_setter(self):
        u = User(password = 'cat')
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = User(password = 'cat')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        u = User(password = 'cat')
        self.assertTrue(u.verify_password('cat'))
        self.assertFalse(u.verify_password('dog'))

    def test_password_salts_are_random(self):
        u = User(password='cat')
        u2 = User(password='cat')
        self.assertTrue(u.password_hash != u2.password_hash)

{% endfilter %}


Content of app/auth/\_\_init.py:

{% filter solution %}
from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import views

{% endfilter %}


Content of app/auth/views.py:

{% filter solution %}
from flask import render_template
from . import auth


@auth.route('/login')
def login():
    return render_template('auth/login.html')

{% endfilter %}


Content of app/auth/forms.py:

{% filter solution %}
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')

{% endfilter %}


Content of app/templates/base.html:

{% filter solution %}
<ul class="nav navbar-nav navbar-right">
    {% if current_user.is_authenticated %}
    <li><a href="{{ url_for('auth.logout') }}">Log Out</a></li>
    {% else %}
    <li><a href="{{ url_for('auth.login') }}">Log In</a></li>
    {% endif %}
</ul>
{% endfilter %}

Content of apps/templates/auth/login.html

{% filter solution %}
{% extends "base.html" %}
{% import "bootstrap/wtf.html" as wtf %}

{% block title %}Flasky - Login{% endblock %}

{% block page_content %}
<div class="page-header">
    <h1>Login</h1>
</div>
<div class="col-md-4">
    {{ wtf.quick_form(form) }}
</div>
{% endblock %}

{% endfilter %}

{% filter solution %}
{% extends "base.html" %}

{% block title %}Flasky{% endblock %}

{% block page_content %}
<div class="page-header">
    <h1>Hello, {% if current_user.is_authenticated %}{{ current_user.username }}{% else %}Stranger{% endif %}!</h1>
</div>
{% endblock %}
{% endfilter %}

5. Create test case for first function (route)
6. Create first function
7. Create basic application that will do following:
	* Allow users to log-in
	* Use Templates
	* Use 	Web Forms
	* Use SQLite or PostreSQL/MySQL
	* Error Handling
	* Use Bootstrap 4
	* Use logging to the console and log file
	* Email Support (sending notification about new sport activity)
	* Allow user to add new kind of sport (like running)
	* Allow user to add new activity and assign it to the sport type
	* Display last ten activities on Dashboard
