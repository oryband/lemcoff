from flask import Flask

from config import debug, secret_key


app = Flask(__name__)
app.config.update(DEBUG=debug,
                  SECRET_KEY=secret_key)


from app import views, admin
