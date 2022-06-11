import psycopg2

import email
from operator import ne
from select import select
from flask import Flask, flash, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash
import config
import sqlite3
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

from babel.dates import format_datetime

hostname = 'postgres-bee2.hostman.site'
database = 'database'
username = 'hostman'
pwd = '4e12f875'
port_id = 5433

app = Flask(__name__)
app.config.from_object(config.config['development'])

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://hostman:4e12f875@143.198.52.41:5433/database"

db = SQLAlchemy(app)

class Clientes(db.Model):

    Cliente_id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(400), unique=False, nullable=False)   
    LastName = db.Column(db.String(60), unique=False, nullable=False)
    Telefone = db.Column(db.String(60), unique=False, nullable=False)
    Email = db.Column(db.String(60), unique=False, nullable=False)
    Address = db.Column(db.String(400), unique=False, nullable=False)

    # def __repr__(self):
    #     return '<User %r>' % self.Cliente_id
class Services(db.Model):

    Service_id = db.Column(db.Integer, primary_key=True)
    Service = db.Column(db.String(400), unique=False, nullable=False)
    Price = db.Column(db.Float, nullable=False)
    Client_id = db.Column(db.Integer, unique=False, nullable=False)
    Name = db.Column(db.String(50), unique=False, nullable=False)
    LastName = db.Column(db.String(60), unique=False, nullable=False)
    Address = db.Column(db.String(400), unique=False, nullable=False)
    is_finished = db.Column(db.String(15), unique=False, nullable=False)
    PayType = db.Column(db.String(15), unique=False, nullable=False)
    service_date = db.Column(db.String(40), unique=False, nullable=False)
    Notes = db.Column(db.String(400), unique=False, nullable=False)
    service_time = db.Column(db.String(60), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.Service_id

events = [

]


new_event = db.session.query(Services.service_date).all()
#print(new_event)
for event in new_event:
  #event = ''.join(str(event).split(','))
  if event == (None,):
    pass
  else:
    event = ''.join(str(event).split(','))
    print(event)
    event_to_add = {
    #'todo': 'timeDate.Service',
    'date': event[2:12],
    'time': event[13:18]
    }
    #if event_to_add.date == 1:
    events.append(event_to_add)
print(events)




















#
#  from flask import Flask, render_template, request, redirect, url_for
# from flask_sqlalchemy import SQLAlchemy
# #import requests
# import config
# import sqlite3
# from werkzeug.security import generate_password_hash, check_password_hash

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///Ymaa.db"

# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)


# class Client(db.Model):

#     Service_id = db.Column(db.Integer, primary_key=True)
#     Service = db.Column(db.String(400), unique=False, nullable=False)
#     price = db.Column(db.Integer, unique=False, nullable=False)
#     Client_id = db.Column(db.Integer, unique=False, nullable=False)
#     Name = db.Column(db.String(50), unique=False, nullable=False)
#     LastName = db.Column(db.String(60), unique=False, nullable=False)
#     Address = db.Column(db.String(400), unique=False, nullable=False)

#     def __repr__(self):
#         return '<User %r>' % self.Service_id


# class Users(db.Model):
  
#     UserID = db.Column(db.Integer, primary_key=True)
#     UserName = db.Column(db.String(50), unique=True, nullable=False)
#     Password = db.Column(db.String(12), unique=False, nullable=False)

#     def __repr__(self):
#         return '<User %r>' % self.user_id





# db.session.add(Users(UserID=None, UserName=email, Password=generate_password_hash(pwd, method='sha256')))
# db.session.commit()






