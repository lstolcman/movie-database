from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import SearchForm

import requests
import math


@app.route('/')
def index():
    #return render_template('main.html')
    return redirect('/search')

@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(url_for('search') + '/' + form.title.data)
    return render_template('search.html', form=form)

@app.route('/search/<title>/<int:page>')
@app.route('/search/<title>', defaults={'page':1})
def search_title(title, page):
    error = None
    pages = None

    fmt = 'http://www.omdbapi.com/?type=movie&s={}&page={}&apikey={}'.format(title, page, app.config['OMDB_APIKEY'])
    response = requests.get(fmt)
    data = response.json()

    if data['Response'] == 'False':
        error = data['Error']
    else:
        pages = range(1, math.ceil(int(data['totalResults'])/10)+1)


    return render_template('search.html', data=data,title=title, error=error, pages=pages)

