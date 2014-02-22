from flask import Flask


DEBUG = True
app = Flask(__name__)
app.secret_key = 'secret'

from app import views, admin


if __name__ == '__main__':
    app.run(debug=DEBUG)
