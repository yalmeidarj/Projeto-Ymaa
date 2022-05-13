from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
#import requests
import config
import sqlite3


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///Ymaa.db"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Client(db.Model):

    Service_id = db.Column(db.Integer, primary_key=True)
    Service = db.Column(db.String(400), unique=False, nullable=False)
    price = db.Column(db.Integer, unique=False, nullable=False)
    Client_id = db.Column(db.Integer, unique=False, nullable=False)
    Name = db.Column(db.String(50), unique=False, nullable=False)
    LastName = db.Column(db.String(60), unique=False, nullable=False)
    Address = db.Column(db.String(400), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.Service_id


print(db.session.query(Client).all())









# class ClientsDB(db.Model):
    

# # table_cols = ['id', 'Name', 'LastName', 'Adress', 'Service', 'price']
#     def get_all(self):
#         self.data = []
#         self.cursor.execute('SELECT * FROM Clients')
#         lis = self.cursor.fetchall()
#         # for row in lis:
#         #     print
#         return lis
#         #print(self.cursor.fetchall())

# # print(DataBasee().get_all())
