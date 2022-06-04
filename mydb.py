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

# conn = psycopg2.connect(
#     host = hostname,
#     dbname = database,
#     user = username,
#     password = pwd,
#     port = port_id
# )


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

c = db.session.query(Clientes.Name).all()
print(c)

# cur =  conn.cursor()
# cur.execute('SELECT * FROM Clientes;')
# clientes = cur.fetchall()
# print(clientes)
# cur.close()

# class Users(UserMixin, db.Model):
  
#     UserID = db.Column(db.Integer, primary_key=True)
#     UserName = db.Column(db.String(50), unique=True, nullable=False)
#     Password = db.Column(db.String(12), unique=False, nullable=False) 

#     def get_id(self):
#            return (self.UserID)

#     def __repr__(self):
#         return '<User %r>' % self.UserID

# class requests(db.Model):
  
#     UserID = db.Column(db.Integer, primary_key=True)
#     Name = db.Column(db.String(50), unique=True, nullable=False)
#     LastName = db.Column(db.String(50), unique=False, nullable=False)
#     UserName = db.Column(db.String(50), unique=True, nullable=False)
#     Password = db.Column(db.String(100), unique=False, nullable=False)

#     def __repr__(self):
#         return '<User %r>' % self.UserID

# class Services(db.Model):

#     Service_id = db.Column(db.Integer, primary_key=True)
#     Service = db.Column(db.String(400), unique=False, nullable=False)
#     Price = db.Column(db.Float, nullable=False)
#     Client_id = db.Column(db.Integer, unique=False, nullable=False)
#     Name = db.Column(db.String(50), unique=False, nullable=False)
#     LastName = db.Column(db.String(60), unique=False, nullable=False)
#     Address = db.Column(db.String(400), unique=False, nullable=False)
#     is_finished = db.Column(db.String(15), unique=False, nullable=False)
#     PayType = db.Column(db.String(15), unique=False, nullable=False)
#     DateTime = db.Column(db.String(40), unique=False, nullable=False)
#     Notes = db.Column(db.String(400), unique=False, nullable=False)

#     def __repr__(self):
#         return '<User %r>' % self.Service_id


# class Expenses(db.Model):
  
#     expense_id = db.Column(db.Integer, primary_key=True)
#     amount = db.Column(db.Float, unique=False, nullable=False)
#     category = db.Column(db.String(50), unique=False, nullable=False)
#     description = db.Column(db.String(150), unique=False, nullable=False)
#     tdate = db.Column(db.String(20), unique=False, nullable=False)
#     type = db.Column(db.String(20), unique=False, nullable=False)
#     is_paid = db.Column(db.String(5), unique=False, nullable=False)

#     def __repr__(self):
#         return '<User %r>' % self.expense_id

# db.create_all()
# 
# db.session.commit()

#conn.close()



















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






