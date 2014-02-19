from flask import render_template

from app import app


@app.route('/')
def index():
    return render_template('index.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    return app.send_static_file('%s.txt' % file_name)


# TODO Render with markdown.
# @app.route('/research/')
# def research():
