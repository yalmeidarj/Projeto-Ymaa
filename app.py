#from crypt import methods
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
#import requests
import config
import sqlite3



def page_not_found(e):
  return render_template('404.html'), 404


app = Flask(__name__)
app.config.from_object(config.config['development'])



app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///Ymaa.db"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


app.register_error_handler(404, page_not_found)

class Clients(db.Model):

    Service_id = db.Column(db.Integer, primary_key=True)
    Service = db.Column(db.String(400), unique=False, nullable=False)
    Price = db.Column(db.Float, nullable=False)
    Client_id = db.Column(db.Integer, unique=False, nullable=False)
    Name = db.Column(db.String(50), unique=False, nullable=False)
    LastName = db.Column(db.String(60), unique=False, nullable=False)
    Address = db.Column(db.String(400), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.Service_id

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

@app.route('/')
def index():
  return render_template('index.html', **locals())


@app.route('/login')
def login():
  return render_template('login.html', **locals())

@app.route('/despesas', methods = ['GET','POST'])
def despesas():
  if request.method == 'POST':
    print('working')
    amount= request.form.get("price")
    category = request.form.get("category__select")
    description = request.form.get("activity")
    date = str(request.form.get("bdate"))
    type_of_payment = request.form.get("payment_type_select")
    is_paid = request.form.get("payment_confirmed_select")
    db.session.add(Expenses(expense_id=None, amount=amount, category=category, description=description, tdate=date, type=type_of_payment, is_paid=is_paid))
    db.session.commit()
    #my_client = db.session.query(Clients).all()
    #db.session.close()

    return redirect(url_for('financeiro'))
  else:
    expense_value = [i[0] for i in db.session.query(Expenses.amount).all()]
    print("Expense value:")
    print(sum(expense_value))
    return render_template('despesas.html', **locals())

@app.route('/financeiro')
def financeiro():
  expense_value = round(sum([i[0] for i in db.session.query(Expenses.amount).all()]), 2)
  pay_received = round(sum([i[0] for i in db.session.query(Clients.Price).all()]), 2)
  print(expense_value, pay_received)
  return render_template('cards.html', **locals())


@app.route('/documentos')
def documentos():
  # username = request.form.get('exampleInputEmail')
  # print(username)
  return render_template('documentos.html', **locals())


@app.route('/registrar')
def register():
  # username = request.form.get('exampleInputEmail')
  # print(username)
  return render_template('register.html', **locals())

@app.route('/servicos', methods = ['GET','POST'])
def services():
  

  my_client = db.session.query(Clients).all()

  print(db.session.query(Clients).all())

  
  if request.method == 'POST':
    print('working')
    service = request.form["Service"]
    price = float(request.form["price"])
    name = request.form["name"]
    lastName = request.form["lastName"]
    address = request.form["address"]
    db.session.add(Clients(Service_id=None, Service=service, Price=price, Client_id=None, Name=name, LastName=lastName, Address=address))
    db.session.commit()
    my_client = db.session.query(Clients).all()
    #db.session.close()

    return redirect(url_for('services'))    
    
    
  return render_template('othertable.html', **locals())




if __name__ == '__main__':
  app.run(host='0.0.0.0', port='8888', debug=True)




