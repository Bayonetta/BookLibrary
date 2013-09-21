import time
from sqlite3 import dbapi2 as sqlite3
from hashlib import md5
from datetime import datetime
from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash, _app_ctx_stack
from werkzeug import check_password_hash, generate_password_hash


#CONFIGURATION
DATABASE = '/home/bayonetta/MyFlask/BookLibrary/book.db'
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

def query_db(query, args=(), one=False):
	cur = get_db().execute(query, args)
	rv = cur.fetchall()
	return (rv[0] if rv else None) if one else rv


def get_user_id(username):
    rv = query_db('select user_id from users where user_name = ?',
                  [username], one=True)
    return rv[0] if rv else None


@app.before_request
def before_request():
	g.user = None
	if 'user_id' in session:
		g.user = session['user_id']

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
			session['user_id'] = app.config['MANAGER_NAME']
			return redirect(url_for('manager'))
	return render_template('manager_login.html', error = error)


@app.route('/reader_login', methods=['GET', 'POST'])
def reader_login(): 
	error = None
	if request.method == 'POST':
		user = query_db('''select * from users where user_name = ?''',
				[request.form['username']], one=True)
		if user is None:
			error = 'Invalid username'
		elif not check_password_hash(user['pwd'], request.form['password']):
			error = 'Invalid password'
		else:
			session['user_id'] = user['user_name']
			return redirect(url_for('reader'))
	return render_template('reader_login.html', error = error)


@app.route('/register', methods=['GET', 'POST'])
def register():
	error = None
	if request.method == 'POST':
		if not request.form['username']:
			error = 'You have to enter a username'
		elif not request.form['password']:
			error = 'You have to enter a password'
		elif request.form['password'] != request.form['password2']:
			error = 'The two passwords do not match'
		elif get_user_id(request.form['username']) is not None:
			error = 'The username is already taken'
		else:
			db = get_db()
			db.execute('''insert into users (user_name, pwd) values (?, ?) ''',
				   [request.form['username'], generate_password_hash(
				request.form['password'])])
			db.commit()
			return redirect(url_for('reader_login'))
	return render_template('register.html', error = error)

@app.route('/logout')
def logout():
	session.pop('user_id', None)
	return redirect(url_for('index'))

@app.route('/manager')
def manager():
	return render_template('manager.html', books = query_db('''
		select * from books''', []))


@app.route('/manager/add', methods=['GET', 'POST'])
def manager_add():
	error = None
	if request.method == 'POST':
		if not request.form['id']:
			error = 'You have to input the book ISBN'
		elif not request.form['name']:
			error = 'You have to input the book name'
		elif not request.form['author']:
			error = 'You have to input the book author'
		elif not request.form['company']:
			error = 'You have to input the publish company'
		elif not request.form['date']:
			error = 'You have to input the publish date'
		else:
			db = get_db()
			db.execute('''insert into books (book_id, book_name, author, publish_com,
				publish_date) values (?, ?, ?, ?, ?) ''', [request.form['id'],
			        request.form['name'], request.form['author'], request.form['company'],
				request.form['date']])
			db.commit()
			return redirect(url_for('manager'))
	return render_template('manager_add.html', error = error)

@app.route('/manager/delete', methods=['GET', 'POST'])
def manager_delete():
	error = None
	if request.method == 'POST':
		if not request.form['id']:
			error = 'You have to input the book name'
		else:
			book = query_db('''select * from books where book_id = ?''',
				[request.form['id']], one=True)
			if book is None:
				error = 'Invalid book id'
			else:
				db = get_db()
				db.execute('''delete from books where book_id=? ''', [request.form['id']])
				db.commit()
				return redirect(url_for('manager'))
	return render_template('manager_delete.html', error = error)			

@app.route('/manager/book/<id>', methods=['GET', 'POST'])
def manager_book(id):
	book = query_db('''select * from books where book_id = ?''', [id], one=True)
       	return render_template('manager_book.html', book = book)


@app.route('/manager/modify/<id>', methods=['GET', 'POST'])
def manager_modify(id):
	error = None
	book = query_db('''select * from books where book_id = ?''', [id], one=True)
	if request.method == 'POST':
		if not request.form['name']:
			error = 'You have to input the book name'
		elif not request.form['author']:
			error = 'You have to input the book author'
		elif not request.form['company']:
			error = 'You have to input the publish company'
		elif not request.form['date']:
			error = 'You have to input the publish date'
		else:
			db = get_db()
			db.execute('''update books set book_name=?, author=?, publish_com=?, publish_date=? where book_id=? ''', [request.form['name'], request.form['author'], request.form['company'], request.form['date'], id])
			db.commit()
			return redirect(url_for('book_index', id = id))
	return render_template('manager_modify.html', book = book, error = error)

@app.route('/reader', methods=['GET', 'POST'])
def reader():
	error = None
	books = None
	if request.method == 'POST':
		if request.form['item'] == 'name':
			if not request.form['query']:
				error = 'You have to input the book name'
			else:
				books = query_db('''select * from books where book_name = ?''',
						[request.form['query']])
				print books
				if not books:
					error = 'Invalid book name'
		else:
			if not request.form['query']:
				error = 'You have to input the book author'
			else:
				books = query_db('''select * from books where author = ?''',
						[request.form['query']])
				if not books:
					error = 'Invalid book author'
	return render_template('reader.html', books = books, error = error)

# @app.route('reader/book/<id>', methods=['GET', 'POST'])
# def reader_index(id):
# 	book = query_db('''select * from books where book_id = ?''', [id], one=True)
#        	return render_template('reader_book.html', book = book)

if __name__ == '__main__':
	init_db()
	app.run()



