# from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask import *
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import sqlite3 as sql

DATABASE = 'account.db'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///account.db'
db = SQLAlchemy(app)

class Contact(db.Model):
    __tablename__ = 'tb_contact'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(80))
    number = db.Column('number', db.String(80))

    def __init__(self, id, name, number):
        self.id = id
        self.name = name
        self.number = number



app.config.from_object(__name__)


app.secret_key = 'final exam'

def connect_db():
    return sql.connect(app.config['DATABASE'])

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to loggin first.')
            return redirect(url_for('login'))
    return wrap

def insert_contact(name, number):
    con = sql.connect(DATABASE)
    cur = con.cursor()
    cur.execute("INSERT INTO tb_contact (name, number) VALUES (?,?)", (name, number))
    con.commit()
    #con.close()

def select_contact(params=()):
    con = sql.connect(DATABASE)
    cur = con.cursor()
    if params==():
        cur.execute("select * from tb_contact")
        return cur.fetchall()
    else:
        string = "select"
        for i in xrange(len(params)-1):
            string += "%s,"
        string += "%s"
        string += " from tb_contact"

        result = cur.execute(string)
        #con.close()
        return result.fetchall()

def select_contact_by_id(contact_id):
    con = sql.connect(DATABASE)
    cur = con.cursor()
    cur.execute("select * from tb_contact where id = ?", (contact_id,))
    #con.close()
    return cur.fetchall()

def update_contact(contact_id, name, number):
    con = sql.connect(DATABASE)
    cur = con.cursor()
    cur.execute("UPDATE tb_contact SET name=?, number=? WHERE id=?", (name, number, contact_id))        
    con.commit()
    #con.close()
    return cur.fetchall()

def delete_contact(contact_id):
    con = sql.connect(DATABASE)
    cur = con.cursor()
    cur.execute("DELETE FROM tb_contact WHERE id=?", (contact_id,))        
    con.commit()
    #con.close()




@app.route('/hello')
@login_required
def hello():
    g.db = connect_db()
    cur = g.db.execute('select name, number from tb_contact')
    contact = [dict(name=row[0], number=row[1]) for row in cur.fetchall()]
    g.db.close()
    return render_template('hello.html', contact=contact, contact_by_id=contact_by_id)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You are logged out.')
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'a' or request.form['password'] != 'a':
            error = 'Invalid Credential. Please try again.'
        else:
            session['logged_in'] = True
            return redirect(url_for('hello'))
    return render_template('login.html', error=error)

@app.route('/contact', methods=['POST', 'GET'])
def contact():
    contact = [dict(id=row[0], name=row[1], number=row[2]) for row in select_contact()]

    error = None
    if request.method == 'POST':
        name = request.form['name']
        number = request.form['number']
        if name == '' or number == '':
            error = 'Invalid! Please input name and number'
        else:
            insert_contact(name, number)
            return redirect(url_for('contact'))
    
    return render_template('contact.html', error=error, contact=contact)

@app.route('/update/<contact_id>', methods=['POST', 'GET'])
def update(contact_id):
    contact = [dict(id=row[0], name=row[1], number=row[2]) for row in select_contact()]
    contact_by_id = [dict(id=row[0], name=row[1], number=row[2]) for row in select_contact_by_id(contact_id)]

    error = None
    if request.method == 'POST':
        name = request.form['name']
        number = request.form['number']
        if name == '' or number == '':
            error = 'Invalid! Please input name and number'
        else:
            update_contact(contact_id, name, number)
            return redirect(url_for('contact'))
    
    return render_template('update.html', error=error, contact=contact, contact_by_id=contact_by_id)

@app.route('/delete/<contact_id>', methods=['POST', 'GET'])
def delete(contact_id):
    if request.method == 'POST':
        delete_contact(contact_id)

    return redirect(url_for('contact'))
    
    #return render_template('contact.html')




if __name__ == '__main__':
    app.run(debug=True)

    
