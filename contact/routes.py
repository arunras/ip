# from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask import *
from functools import wraps
import sqlite3

DATABASE = 'account.db'

app = Flask(__name__)

app.config.from_object(__name__)


app.secret_key = 'final exam'

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

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



@app.route('/hello')
@login_required
def hello():
    g.db = connect_db()
    cur = g.db.execute('select name, number from tb_contact')
    contact = [dict(name=row[0], number=row[1]) for row in cur.fetchall()]
    g.db.close()
    return render_template('hello.html', contact=contact)

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
    g.db = connect_db()
    cur = g.db.execute('select id, name, number from tb_contact')
    contact = [dict(id=row[0], name=row[1], number=row[2]) for row in cur.fetchall()]

    error = None
    if request.method == 'POST':
        name = request.form['name']
        number = request.form['number']
        if name == '' or number == '':
            error = 'Invalid! Please input name and number'
        else:
            g.db.execute('insert into tb_contact(id, name, number) values (NULL,?,?)',(name, number))
            g.db.commit()
            return redirect(url_for('contact'))
    
    g.db.close()
    return render_template('contact.html', error=error, contact=contact)


if __name__ == '__main__':
    app.run(debug=True)

    
