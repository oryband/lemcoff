#!/usr/bin/env python

import os.path
import sqlite3

from flask import Flask, render_template, g
from flask.ext.admin import Admin
from flask.ext.sqlalchemy import SQLAlchemy

# Configuration
DEBUG = True
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(APP_ROOT, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(APP_ROOT, 'db_repository')

app = Flask(__name__)
admin = Admin(app)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_to_database()
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
def hello_world():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=DEBUG)
