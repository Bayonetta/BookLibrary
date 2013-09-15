import time
from sqlite3 import dbapi2 as sqlite3
from hashlib import md5
from datetime import datetime
from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash, _app_ctx_stack
from werkzeug import check_password_hash, generate_password_hash


#CONFIGURATION
DATABASE = '/tmp/book.db'
DEBUG = True
SECRET_KEY = 'development key'
MANAGER_NAME = 'admin'
MANAGER_PWD = '123456'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def get_db():
	top = _app_ctx_stack.top
	if not hasattr(top, 'sqlite_db'):
		top.sqlite_db = sqlite3.connect(app.config['DATABASE'])
		top.sqlite_db.row_factory = sqlite3.Row
        return top.sqlite_db

@app.teardown_appcontext
def close_database(exception):
	top = _app_ctx_stack.top
	if hasattr(top, 'sqlite_db'):
		top.sqlite_db.close()

def init_db():
	with app.app_context():
		db = get_db()
		with app.open_resource('book.sql', mode='r') as f:
			db.cursor().executescript(f.read())
		db.commit()


@app.route('/')
def index():
        return render_template('index.html')

@app.route('/manager_login', methods=['GET', 'POST'])
def manager_login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != app.config['MANAGER_NAME']:
			error = 'Invalid username'
		elif request.form['password'] != app.config['MANAGER_PWD']:
			error = 'Invalid password'
		else:
			flash('Manager Login')
			return redirect(url_for('manager'))
	return render_template('manager_login.html', error = error)


@app.route('/reader_login', methods=['GET', 'POST'])
def reader_login():
	return render_template('reader_login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
	return render_template('register.html')


@app.route('/manager')
def manager():
	return render_template('manager.html')


if __name__ == '__main__':
	init_db()
	app.run()



