from flask import render_template, flash, redirect
from app import app
from app.forms import SearchForm


@app.route('/')
def index():
    #return render_template('main.html')
    return redirect('/search')

@app.route('/search', methods=['GET', 'POST'])
def search():
    data = None
    form = SearchForm()
    if form.validate_on_submit():
        data = {'title':'asd'}
    return render_template('search.html', form=form, data=data)

