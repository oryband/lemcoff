import os.path as op

from flask import Flask


app = Flask(__name__)
app.config.from_object('config')

path = op.dirname(__file__)
static = op.join(path, 'static')

from app import views, admin


if __name__ == '__main__':
    app.run(debug=True)
