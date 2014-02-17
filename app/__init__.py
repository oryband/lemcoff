from flask import Flask
from flask.ext.mongoengine import MongoEngine
from flask.ext.admin import Admin


app = Flask(__name__)
app.config.from_object('config')
db = MongoEngine(app)

from app import views, models, admin


if __name__ == '__main__':
    app.run(debug=True)
