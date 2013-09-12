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

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)



@app.route('/')
def index():
        return render_template('index.html')

@app.route('/manager_login', methods=['GET', 'POST'])
def manager_login():
	return render_template('login.html')


@app.route('/reader_login', methods=['GET', 'POST'])
def reader_login():
	return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
	return render_template('register.html')


if __name__ == '__main__':
	app.run()



