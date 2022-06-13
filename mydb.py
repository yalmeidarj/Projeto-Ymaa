import psycopg2
import datetime
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

    def __repr__(self):
        return '<User %r>' % self.Cliente_id

class Expenses(db.Model):
  
    expense_id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, unique=False, nullable=False)
    category = db.Column(db.String(50), unique=False, nullable=False)
    description = db.Column(db.String(150), unique=False, nullable=False)
    tdate = db.Column(db.String(20), unique=False, nullable=False)
    type = db.Column(db.String(20), unique=False, nullable=False)
    is_paid = db.Column(db.String(5), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.expense_id

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

today = datetime.datetime.today()
past_week = today - datetime.timedelta(days=9)
past_30days = today - datetime.timedelta(days=30)
list_past_week = db.session.query(Services).filter(Services.service_date.between(str(past_week), str(today))).all()
list_past_30days = db.session.query(Services).filter(Services.service_date.between(str(past_30days), str(today))).all()

expenses_past_week = db.session.query(Expenses).filter(Expenses.tdate.between(str(past_week), str(today))).all()
expenses_past_30days = db.session.query(Expenses).filter(Expenses.tdate.between(str(past_30days), str(today))).all()


sum_past_week = round(sum([i.Price for i in list_past_week]), 2)
sum_past_30days = round(sum([i.Price for i in list_past_30days]), 2)

expenses_sum_past_week = round(sum([i.amount for i in expenses_past_week]), 2)
expenses_sum_past_30days = round(sum([i.amount for i in expenses_past_30days]), 2)

balance_past_week = sum_past_week - expenses_sum_past_week
balance_past_30days = sum_past_30days - expenses_sum_past_30days

report = f'Total made and spent last week: {sum_past_week}/ {expenses_sum_past_week}\nTotal made and spent last 30 days: {sum_past_30days}/ {expenses_sum_past_30days}\nBalance last week: {balance_past_week }\nBalance last 30 days: {balance_past_30days}'
print(report)


