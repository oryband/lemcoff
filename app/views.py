from flask import render_template

from app import app, models


@app.route('/')
def index():
    return render_template('index.html')


def render_page(page):
    entries = models.Entry.objects(page=page)
    return render_template('page.html', page=page, entries=entries)


@app.route('/research/')
def research():
    page = models.Page.objects(title='research').get()
    return render_page(page)


@app.route('/publications/')
def publications():
    page = models.Page.objects(title='publications').get()
    return render_page(page)


@app.route('/members/')
def members():
    page = models.Page.objects(title='members').get()
    return render_page(page)


@app.route('/community/')
def community():
    page = models.Page.objects(title='community').get()
    return render_page(page)


@app.route('/links/')
def links():
    page = models.Page.objects(title='links').get()
    return render_page(page)
