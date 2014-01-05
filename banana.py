#imports

import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.heroku import Heroku #handles URL configs
from contextlib import closing
import twilio.twiml
import parser
import os

#configs
DATABASE = '/tmp/banana.db'
DEBUG = True
SECRET_KEY = 'oscar and bambi'
USERNAME = 'admin'
PASSWORD = '12345'

#creating app
app = Flask(__name__)
app.config.from_object(__name__)
#app.config.from_envvar('BANANA_SETTINGS', silent=True)
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)
heroku = Heroku(app)

#database stuff
# def connect_db():
#     return sqlite3.connect(app.config['DATABASE'])

# def init_db():
#     with closing(connect_db()) as db:
#         with app.open_resource('schema.sql', mode='r') as f:
#             db.cursor().executescript(f.read())
#         db.commit()

# @app.before_request
# def before_request():
#     g.db = connect_db()

# @app.teardown_request
# def teardown_request(exception):
#     db = getattr(g, 'db', None)
#     if db is not None:
#         db.close()


#ROUTING
@app.route('/home')
def home():
    return "hello world"

@app.route('/hello', methods=['GET', 'POST'])
def banana():
    message = "hi"
    resp = twilio.twiml.Response()
    resp.message(message)
    return str(resp)

@app.route('/text', methods=['GET', 'POST'])
def hello_text():
    body = request.values.get('Body', None)
    parsed = parser.sms_parser(body)
    if parsed:
        (user_phone, contact) = parsed
        contact_phone = retrieve_phone(user_phone, contact)
        message = contact_phonel
    else:
        message = "Incorrect format. Please try again with <your number> <contact name> <pin>"
    
    resp = twilio.twiml.Response()
    resp.message(message)
    return str(resp)

@app.route('/test', methods=['GET','POST'])
def blah():
    user = User.query.all()[0]
    return user.id, user.phone, user.contacts

#MODELS

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.Integer, unique=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    contacts = db.relationship('Contact')

    #TODO: Add password

    def __init__(self, phone, username, email):
        self.phone= phone
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    phone = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, name, phone, user_id):
        self.name = name
        self.phone= phone
        self.user_id = user_id

#TODO: THIS IS HELLA JANKY. fix
def retrieve_phone(user_phone, contact_name):
    user = User.query.filter_by(phone=user_phone).first()
    contact = Contact.query.filter_by(name=contact_name, user_id= user.id).first()
    return contact.phone

if __name__ == '__main__':
    app.run(host='0.0.0.0')
