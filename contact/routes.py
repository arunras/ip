from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps

app = Flask(__name__)

app.secret_key = 'final exam'

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
    return render_template('hello.html')

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



if __name__ == '__main__':
    app.run(debug=True)

    
