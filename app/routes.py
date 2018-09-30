from flask import render_template, flash, redirect
from app import app
from app.forms import SearchForm

import requests


@app.route('/')
def index():
    #return render_template('main.html')
    return redirect('/search')

@app.route('/search', methods=['GET', 'POST'])
def search():
    data = None
    error = None
    form = SearchForm()
    if form.validate_on_submit():
        fmt = 'http://www.omdbapi.com/?s={}&apikey={}'.format(form.title.data, app.config['OMDB_APIKEY'])
        response = requests.get(fmt)
        data = response.json()
        if data['Response'] == 'False':
            error = data['Error']
    return render_template('search.html', form=form, data=data, error=error)



