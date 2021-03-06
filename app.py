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
from sqlalchemy.engine import result
import sqlalchemy
from sqlalchemy import create_engine, MetaData,\
Table, Column, Numeric, Integer, VARCHAR, update


def page_not_found(e):
  return render_template('404.html'), 404

app = Flask(__name__)
app.config.from_object(config.config['development'])

##### Db config 
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://hostman:4e12f875@143.198.52.41:5433/database"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

engine = create_engine("postgresql://hostman:4e12f875@143.198.52.41:5433/database")
 
# initialize the Metadata Object
meta = MetaData(bind=engine)
MetaData.reflect(meta)

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
    service_date = db.Column(db.String(40), unique=False, nullable=False)
    Notes = db.Column(db.String(400), unique=False, nullable=False)
    service_time = db.Column(db.String(60), unique=False, nullable=False)

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


def fetch():
  day_today = datetime.datetime.today()
  yesterday = day_today - datetime.timedelta(days=1)
  events = []

  todays_events = db.session.query(Services).all()

  indx = 0
  for event in todays_events:
      
      event_to_add = {
      'todo': f'{todays_events[indx].Name} - {todays_events[indx].Address}',
      'date': todays_events[indx].service_date,
      'time': todays_events[indx].service_time,
      'service': todays_events[indx].Service,
      'notes': todays_events[indx].Notes,
      }
      events.append(event_to_add)
      indx += 1
  events = sorted(events, key=lambda event: event['time'])
  return events


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
        flash('Credenciais n??o autorizadas. Tente novamente ou entre em contato com o Administrador')
        return redirect(url_for('login'))
    else:
      flash('Usu??rio n??o existente. Tente novamente ou entre em contato com o Administrador')
  return render_template('login.html', **locals())

@app.route('/logout')
@login_required
def logout():
  logout_user()
  flash('Sess??o encerrada com sucesso!')
  return redirect(url_for('login'))

@app.route('/registrar' , methods = ['GET','POST'])
def registrar():  
  if request.method =='POST':
    error = None 
    userName = request.form.get("email") 
    userName = db.session.query(Users).filter_by(UserName=userName).first()
    if userName:      
      flash('Email j?? registrado. Use outro Email ou entre em sua conta.')
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
        flash('Pedido de registro de conta efetivado. Por favor, aguarde at?? que a Administra????o aprove seu registro antes de entrar em sua conta.')
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
  #events = sorted(events, key=lambda event: event['time'])
  return render_template('calendar.html', events=fetch())

@app.route('/timeline', methods = ['GET','POST'])
@login_required
def timeline():  
  def fetch_events(date:datetime.date = datetime.date.today() ):
    chosen_date = date
    previous_day = chosen_date - datetime.timedelta(days=1)
    events = []
    events_db = db.session.query(Services).filter(Services.service_date.between(str(previous_day), str(chosen_date))).all()
    indx = 0
    for event in events_db:
        
        event_to_add = {
        'todo': f'{events_db[indx].Name} - {events_db[indx].Address}- {events_db[indx].Service}',
        'date': events_db[indx].service_date,
        'time': events_db[indx].service_time,
        'service': events_db[indx].Service,
        'notes': events_db[indx].Notes,
        }
        events.append(event_to_add)
        indx += 1
    events = sorted(events, key=lambda event: event['time'])
    return events
  if request.method == 'POST':
    if request.form.get("newdate") != '':
      chosen_day = datetime.datetime.strptime(request.form.get("newdate"), '%Y-%m-%d')
      date_to_display = str(chosen_day)[:10] 
      fetch_events(chosen_day)

      return render_template('timeline.html', events = fetch_events(chosen_day),  **locals())
    else:
      chosen_day = datetime.datetime.today()
      date_to_display = str(chosen_day)[:10] 
      fetch_events(chosen_day)

      return render_template('timeline.html', events = fetch_events(chosen_day),  **locals())
  else:
    chosen_day = datetime.datetime.today()
    date_to_display = str(chosen_day)[:10]

    return render_template('timeline.html', events = fetch_events(chosen_day),  **locals())

@app.route('/despesas', methods = ['GET','POST'])
@login_required
def despesas():
  if request.method == 'POST':    
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
    
    return render_template('despesas.html', **locals())

@app.route('/financeiro')
@login_required
def financeiro():
  day_today = datetime.datetime.today()
  yesterday = day_today - datetime.timedelta(days=1)
  past_week = day_today - datetime.timedelta(days=7)
  past_30days = day_today - datetime.timedelta(days=30)

  money_today = db.session.query(Services).filter(Services.service_date.between(str(yesterday), str(day_today))).all() 
  cost_today = db.session.query(Expenses).filter(Expenses.tdate.between(str(yesterday), str(day_today))).all()
  pay_today = round(sum([i.Price for i in money_today]), 2)
  expense_today = round(sum([i.amount for i in cost_today]), 2)

  expenses_past_week = db.session.query(Expenses).filter(Expenses.tdate.between(str(past_week), str(day_today))).all()
  expenses_past_30days = db.session.query(Expenses).filter(Expenses.tdate.between(str(past_30days), str(day_today))).all()
  list_past_week = db.session.query(Services).filter(Services.service_date.between(str(past_week), str(day_today))).all()
  list_past_30days = db.session.query(Services).filter(Services.service_date.between(str(past_30days), str(day_today))).all()

  sum_past_week = round(sum([i.Price for i in list_past_week]), 2)
  sum_past_30days = round(sum([i.Price for i in list_past_30days]), 2)

  expenses_sum_past_week = round(sum([i.amount for i in expenses_past_week]), 2)
  expenses_sum_past_30days = round(sum([i.amount for i in expenses_past_30days]), 2)

  balance_past_week = sum_past_week - expenses_sum_past_week
  balance_past_30days = sum_past_30days - expenses_sum_past_30days

  # money_today = db.session.query(Services).filter(Services.service_date == str(day_today)).all()  
  # cost_today = db.session.query(Expenses).filter(Expenses.tdate == str(day_today)).all()
  
  # expense_today = round(sum([i.Price for i in money_today]), 2)
  # pay_today = round(sum([i.Price for i in cost_today]), 2)

  expense_value_today = "${:,.2f}".format(round(sum([i[0] for i in db.session.query(Expenses.amount).all()]), 2))
  pay_received_today = "${:,.2f}".format(round(sum([i[0] for i in db.session.query(Services.Price).all()]), 2))
  balance_today = round(pay_today - expense_today, 2)
  service_id = Clientes.Cliente_id

  
  return render_template('financeiro.html', **locals())

@app.route('/tf')
@login_required
def tf():
  day_today = datetime.datetime.today()
  past_week = day_today - datetime.timedelta(days=9)
  past_30days = day_today - datetime.timedelta(days=30)
  expenses_past_week = db.session.query(Expenses).filter(Expenses.tdate.between(str(past_week), str(day_today))).all()
  expenses_past_30days = db.session.query(Expenses).filter(Expenses.tdate.between(str(past_30days), str(day_today))).all()
  list_past_week = db.session.query(Services).filter(Services.service_date.between(str(past_week), str(day_today))).all()
  list_past_30days = db.session.query(Services).filter(Services.service_date.between(str(past_30days), str(day_today))).all()

  sum_past_week = round(sum([i.Price for i in list_past_week]), 2)
  sum_past_30days = round(sum([i.Price for i in list_past_30days]), 2)

  expenses_sum_past_week = round(sum([i.amount for i in expenses_past_week]), 2)
  expenses_sum_past_30days = round(sum([i.amount for i in expenses_past_30days]), 2)

  balance_past_week = sum_past_week - expenses_sum_past_week
  balance_past_30days = sum_past_30days - expenses_sum_past_30days
  
   
  expense_today = round(sum([i[0] for i in db.session.query(Expenses.amount).all()]), 2)
  pay_today = round(sum([i[0] for i in db.session.query(Services.Price).all()]), 2)
  expense_value_today = "${:,.2f}".format(round(sum([i[0] for i in db.session.query(Expenses.amount).all()]), 2))
  pay_received_today = "${:,.2f}".format(round(sum([i[0] for i in db.session.query(Services.Price).all()]), 2))
  balance_today = round(pay_today - expense_today, 2)
  service_id = Clientes.Cliente_id


  return render_template('testingdespesas.html', **locals())

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
      schedule = ''.join(str(date_time).split(','))
      date = schedule[:10]
      time = schedule[11:18]
      notes = request.form.get("comments")

      db.session.add(Services(Service_id=None, Service=description_service, Price=price,
      Client_id=clientID, Name=my_client.Name, LastName=my_client.LastName, Address=my_client.Address,
      is_finished=pay_confirm, PayType=pay_type, service_date=date, service_time=time, Notes=notes ))

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

      # Feed 'Services' Table
      description_service = request.form.get('service2')
      price = request.form.get('price2')
      pay_confirm = request.form.get('payment_confirmed2')
      pay_type = request.form.get("payment_type2")
      date_time = request.form.get("meeting-time2")            
      schedule = ''.join(str(date_time).split(','))
      date = schedule[:10]
      time = schedule[11:18]
      notes = request.form.get("comments2")

      db.session.add(Services(Service_id=None, Service=description_service, Price=price, 
      Client_id=last.Cliente_id, Name=last.Name, LastName=last.LastName, Address=last.Address,
      is_finished=pay_confirm, PayType=pay_type, service_date=date, service_time=time, Notes=notes ))

      db.session.commit()

    return redirect(url_for('servicos'))
  return render_template('alternative_servicos.html', **locals())

@app.route('/servicos', methods = ['GET','POST'])
@login_required
def servicos(): 

  all_services = db.session.query(Services).all()
  c = ''
  #select = request.form.get('comp_select')
  if request.method == 'POST':
    print("i'm working")
  if request.form.get("confirm_pay") == "N??o":
    # my_service = meta.tables['services']
    # u = update(my_service)
    # u = u.values({"is_finished": "Sim"})
    # u = u.where(my_service.c.Service_id == request.form.get("book_id"))
    # engine.execute(u)
    
    # db.session.commit()
    return redirect(url_for('servicos'))
    #print('Book ID: ', request.form.get('confirm_pay'))
  elif request.form.get('s_id'):
    c = request.form.get("sid")
    print(c)

    
    
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

@app.route('/client_view')
@login_required
def client_view(client):
   
  return render_template('client_view.html', client=client, **locals())

if __name__ == '__main__':
  app.run(host='0.0.0.0', port='8888', debug=True)




