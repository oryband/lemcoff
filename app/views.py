from flask import render_template
from flask_flatpages import FlatPages

from app import app


# Settings
FLATPAGES_AUTO_RELOAD = False
FLATPAGES_EXTENSION = '.md'
app.config.from_object(__name__)


flatpages = FlatPages(app)


@app.route('/')
def index():
    page = flatpages.get_or_404('index')
    return render_template('index.html', page=page, name='index')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    return app.send_static_file('%s.txt' % file_name)


@app.route('/<name>/')
def post(name):
    page = flatpages.get_or_404(name)
    return render_template('page.html', page=page, name=name)
