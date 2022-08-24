
# from flask_app.models.likes import Likes
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.users import User
from flask_app.models.cars import Cars
from flask import render_template, redirect, session, flash, request
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/success', methods=['POST'])
def register_account():
    if not User.validate_register(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'password' : pw_hash
    }
    
    user = User.add_one(data)
    session['user_id'] = user
    return redirect('/cars')

@app.route('/login', methods=['POST'])
def login():
    
    data = {"email" : request.form['email']}
    user_db = User.get_by_email(data)
    if not user_db:
        flash("Invalid Email or Password")
        return redirect('/')
    if not bcrypt.check_password_hash(user_db.password, request.form['password']):
        flash("Invalid Email or Password")
        return redirect('/')
    session['user_id'] = user_db.id
    return redirect('/cars')

@app.route('/cars')
def home_page():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id' : session['user_id']
    }
    
    
    return render_template('dashboard.html', user = User.get_by_id(data), cars = Cars.get_all())

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/cars/<int:id>')
def display(id):
    
    data = {
        'id' : id
    }

    return render_template('display.html', cars = Cars.get_all(), user = User.get_by_id(data), id = data['id'])

@app.route('/cars/new')
def create_show():
    return render_template('create.html')

@app.route('/submit', methods=['POST'])
def submit():
    
    if not Cars.validate_car(request.form):
        return redirect('/cars/new')
    data = {
        'model' : request.form['model'],
        'year' : request.form['year'],
        'make' : request.form['make'],
        'description' : request.form['description'],
        'creator_id' : session['user_id'],
        'price' : request.form['price']

    }
    Cars.add_one(data)
    return redirect('/cars')

@app.route('/cars/edit/<int:id>')
def edit_page(id):
    data = {
        'id' : id
    }
    return render_template("edit.html", cars = Cars.get_by_id(data))


@app.route('/edit/submit/<int:id>', methods=['POST'])
def edit(id):
    session['id'] = id
    if not Cars.validate_car(request.form):
        return redirect('/cars/edit/' + str(session['id']))
    data = {
        'model' : request.form['model'],
        'year' : request.form['year'],
        'make' : request.form['make'],
        'description' : request.form['description'],
        'creator_id' : request.form['id'],
        'price' : request.form['price']

    }
    Cars.edit(data)
    return redirect('/cars')

@app.route('/delete/<int:id>')
def delete_show(id):
    data = {
        'id' : id
    }
    Cars.delete(data)
    return redirect('/cars')
