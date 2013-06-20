from flask import *
from functools import wraps
import sqlite3

DATABASE = 'message.db'

app = Flask(__name__)
app.config.from_object(__name__)

app.secret_key = "my key"

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

@app.route('/')
def home():
    return render_template('home.html')


def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to Login First.')
            return redirect(url_for('log'))
    return wrap

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('log'))


@app.route('/message')
@login_required
def message():
    g.db = connect_db()
    cur = g.db.execute('select msg_msg from msg')
    message = [dict(msg_msg=row[0]) for row in cur.fetchall()]
    return render_template('message.html', message=message)


@app.route('/log', methods=['GET', 'POST'])
def log():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'username' or request.form['password'] !='password':
            error = 'Invalid Entry, Please Try Again.'
        else:
            session['logged_in'] = True
            return redirect(url_for('message'))
    return render_template('log.html' , error=error)

@app.route('/message', methods=['POST'])
def add_entry():
    g.db = connect_db()
    cur = g.db.execute('insert into msg (msg_msg) values (?)', [request.form['input_msg']])
    g.db.commit()
    flash('New Entry was SUCCESSFULLY POSTED.')
    return redirect(url_for('message'))




if __name__ == '__main__':
    app.run(debug=True)
