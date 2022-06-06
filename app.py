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
import datetime
from babel.dates import format_datetime



def page_not_found(e):
  return render_template('404.html'), 404

app = Flask(__name__)
app.config.from_object(config.config['development'])

##### Db config 
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://hostman:4e12f875@143.198.52.41:5433/database"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(UserID):
    return Users.query.get(UserID)




class Users(UserMixin, db.Model):
  
    UserID = db.Column(db.Integer, primary_key=True)
    UserName = db.Column(db.String(50), unique=True, nullable=False)
    Password = db.Column(db.String(12), unique=False, nullable=False)

    def get_id(self):
           return (self.UserID)

    def __repr__(self):
        return '<User %r>' % self.UserID

class requests(db.Model):
  
    UserID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(50), unique=True, nullable=False)
    LastName = db.Column(db.String(50), unique=False, nullable=False)
    UserName = db.Column(db.String(50), unique=True, nullable=False)
    Password = db.Column(db.String(100), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.UserID

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
    DateTime = db.Column(db.String(40), unique=False, nullable=False)
    Notes = db.Column(db.String(400), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.Service_id

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
#Session = sessionmaker(bind=some_engine)
events = [
    # {
    #     'todo' : 'task',
    #     'date' : '2022-05-17',
    #     'time' : '20:26'
    # },
    # {
    #     'todo' : 'task2',
    #     'date' : '2022-05-17',
    #     'time' : '15:26'
    # },    
    # {
    #     'todo' : 'task3',
    #     'date' : '2022-05-22',
    # },
    # {
    #     'todo' : 'task4',
    #     'date' : '2022-06-17',
    # },
    # {
    #     'todo' : 'task6',
    #     'date' : '2022-05-17',
    # }
]


new_event = db.session.query(Services.DateTime).all()
print(new_event)
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
    events.append(event_to_add)
print(events)
# DATETIMES = db.session.query(Services.DateTime).all()
# # n = ''.join(str(DATETIMES).split(','))
# # print(n)
# for timeDate in DATETIMES :
#   timeDate = ''.join(str(timeDate).split(','))
#   print(timeDate)
#   if timeDate != '(None)':
#     new_event = {
#     'todo': 'timeDate.Service',
#     'date': timeDate[:12],
#     'time': timeDate[13:18]
#     }
#     events.append(new_event)
#   else:
#     print('nothing')
    
#   print(events)

############################
app.register_error_handler(404, page_not_found)

@app.route('/', methods = ['GET','POST'])
def login():
  error = None
  if request.method =='POST':
    userName = request.form.get("email")
    password = request.form.get("password")
    user = db.session.query(Users).filter_by(UserName=userName).first()
    if user:
      if check_password_hash(user.Password, password):
        login_user(user, remember=True)
        return redirect(url_for('home'))
      else:
        flash('Credenciais não autorizadas. Tente novamente ou entre em contato com o Administrador')
        return redirect(url_for('login'))
    else:
      flash('Usuário não existente. Tente novamente ou entre em contato com o Administrador')
  return render_template('login.html', **locals())

@app.route('/logout')
@login_required
def logout():
  logout_user()
  flash('Sessão encerrada com sucesso!')
  return redirect(url_for('login'))

@app.route('/registrar' , methods = ['GET','POST'])
def registrar():  
  if request.method =='POST':
    error = None 
    userName = request.form.get("email") 
    userName = db.session.query(Users).filter_by(UserName=userName).first()
    if userName:
      print('usuario existente')
      flash('Email já registrado. Use outro Email ou entre em sua conta.')
      # Account already exists.

    else:
      name = request.form.get("name")
      last_name = request.form.get("lastname")
      userName = request.form.get("email")
      password = request.form.get("password")
      password_confirm = request.form.get("password_confirm")
      if password == password_confirm:
        # password confirmed
        password_hash = generate_password_hash(password, method='sha256')
        db.session.add(requests(UserID=None, Name=name, LastName=last_name, UserName=userName, Password=password_hash))
        db.session.commit()
        flash('Pedido de registro de conta efetivado. Por favor, aguarde até que a Administração aprove seu registro antes de entrar em sua conta.')
        return redirect(url_for('registrar'))
      else:
        flash('Senha divergente. Por favor, verique sua senha e repita a MESMA senha para o cadastro.')
        return redirect(url_for('registrar'))

  return render_template('register.html', **locals())

@app.route('/home')
@login_required
def home():
  return render_template('home.html', **locals())

@app.route('/calendar')
@login_required
def calendar():
  #global events
  # date format YYYY-MM-DD
  #events=events
  return render_template('calendar.html', events=events)

@app.route('/timeline')
@login_required
def timeline():
  today = datetime.datetime.today().strftime
  #today_ptBR = format_datetime(today, format='full')
  #events = events 
  #global events
  # date format YYYY-MM-DD
  #events=events
  return render_template('timeline.html',events = events,  **locals())

@app.route('/despesas', methods = ['GET','POST'])
@login_required
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

    return redirect(url_for('financeiro'))
  else:
    expense_value = [expense[0] for expense in db.session.query(Expenses.amount).all()]
    print("Expense value:")
    print(sum(expense_value))

    return render_template('despesas.html', **locals())

@app.route('/financeiro')
@login_required
def financeiro():
   
  expense = round(sum([i[0] for i in db.session.query(Expenses.amount).all()]), 2)
  pay = round(sum([i[0] for i in db.session.query(Services.Price).all()]), 2)
  expense_value = "${:,.2f}".format(round(sum([i[0] for i in db.session.query(Expenses.amount).all()]), 2))
  pay_received = "${:,.2f}".format(round(sum([i[0] for i in db.session.query(Services.Price).all()]), 2))
  balance = "${:,.2f}".format(round(pay - expense, 2))
  service_id = Clientes.Cliente_id
  # def getme():
  #   db.session.query(Clientes.Cliente_id where expense)


  return render_template('cards.html', **locals())

@app.route('/documentos')
@login_required
def documentos():
  return render_template('documentos.html', **locals())

@app.route('/al', methods = ['GET','POST'])
@login_required
def al():
  if request.method =="POST":
    select = request.form.get('mval')
    
    if select == 'no':
      # Fetch from 'Clientes' Table
      # get from table, NOT FEED
      clientID = request.form.get("ClientID")
      my_client = db.session.query(Clientes).filter_by(Cliente_id=clientID).first()

      # Feed 'Services' Table
      description_service = request.form.get('service')
      price = request.form.get('price')
      pay_confirm = request.form.get('payment_confirmed')
      pay_type = request.form.get("payment_type")
      date_time = request.form.get("meeting-time")
      notes = request.form.get("comments")
      db.session.add(Services(Service_id=None, Service=description_service, Price=price, Client_id=clientID, Name=my_client.Name, LastName=my_client.LastName, Address=my_client.Address, is_finished=pay_confirm, PayType=pay_type, DateTime=date_time, Notes=notes ))
      db.session.commit()
    
    else:
      # Feed 'Clientes' Table
      name = request.form.get('name')
      lastName = request.form.get('lastName')
      phone = request.form.get("phone")
      email = request.form.get("email")
      address = request.form.get("address")      
      db.session.add(Clientes(Cliente_id=None, Name=name, LastName=lastName, Telefone=phone, Email=email, Address=address))
      db.session.commit()      

      # get clientID from last record in "Clientes"
      #client = db.session.query(func.max(Clientes.Cliente_id)).first().select()
      last = db.session.query(Clientes).order_by(Clientes.Cliente_id.desc()).first()
      print(last,type(last))
      print(last.Name)
      #last = db.session.query(Clientes).filter_by(client).first()
      #print(last)


      # Feed 'Services' Table
      description_service = request.form.get('service2')
      price = request.form.get('price2')
      pay_confirm = request.form.get('payment_confirmed2')
      pay_type = request.form.get("payment_type2")
      date_time = request.form.get("meeting-time2")
      notes = request.form.get("comments2")
      db.session.add(Services(Service_id=None, Service=description_service, Price=price, Client_id=last.Cliente_id, Name=last.Name, LastName=last.LastName, Address=last.Address, is_finished=pay_confirm, PayType=pay_type, DateTime=date_time, Notes=notes ))
      db.session.commit()

    return redirect(url_for('servicos'))
  return render_template('alternative_servicos.html', **locals())

@app.route('/servicos', methods = ['GET','POST'])
@login_required
def servicos():
  
  

  all_services = db.session.query(Services).all()

  print(db.session.query(Services).all())
  select = request.form.get('comp_select')
  print(select)
  if request.method == 'POST':    
    if x:
      new_client = False      
      print('working')
      service = request.form["Service"]
      price = float(request.form["price"])
      name = request.form["name"]
      lastName = request.form["lastName"]
      address = request.form["address"]
      db.session.add(Services(Service_id=None, Service=service, Price=price, Client_id=None, Name=name, LastName=lastName, Address=address, is_finished=0))
      db.session.commit()
      all_services = db.session.query(Services).all()

      return redirect(url_for('servicos'))  
    else:
      new_client = True
      service = request.form["Service"]
      price = float(request.form["price"])
      
      
      return redirect(url_for('servicos'))  
    
    
  return render_template('servicos.html', **locals())

@app.route('/clientes', methods = ['GET','POST'])
@login_required
def clientes():
  
  clientes = db.session.query(Clientes).all()
  
  if request.method == 'POST':
    
    name = request.form["name"]
    lastName = request.form["lastName"]
    telefone = request.form["telefone"]
    email = request.form["email"]
    address = request.form["address"]
    db.session.add(Clientes(Cliente_id=None, Name=name, LastName=lastName, Telefone=telefone, Email=email, Address=address))
    db.session.commit()
    clientes = db.session.query(Clientes).all()
    #db.session.close()

    return redirect(url_for('clientes'))    
    
    
  return render_template('clientes.html', **locals())


if __name__ == '__main__':
  app.run(host='0.0.0.0', port='8888', debug=True)




