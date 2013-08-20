from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, world!'

@app.route('/hello')
def hello_world1():
    return 'hahahhahahaha'

if __name__ == '__main__':
    app.run()
