from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required

from app import app, db
from app.forms import SearchForm, LoginForm, RegistrationForm
from app.models import User, Favourite

import requests
import math



@app.route('/')
def index():
    return render_template('main.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))



@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(url_for('search') + '/' + form.title.data)
    return render_template('search.html', form=form)


@app.route('/search/<title>/<int:page>')
@app.route('/search/<title>', defaults={'page':1})
@login_required
def search_title(title, page):
    error = None
    pages = None

    fmt = 'http://www.omdbapi.com/?type=movie&s={}&page={}&apikey={}'.format(title, page, app.config['OMDB_APIKEY'])
    response = requests.get(fmt)
    data = response.json()

    if data['Response'] == 'False':
        flash(data['Error'])
    else:
        pages = range(1, math.ceil(int(data['totalResults'])/10)+1)

    return render_template('search.html', data=data, title=title, error=error, pages=pages)


@app.route('/details/<imdb_id>')
@login_required
def details(imdb_id):
    error = None

    fmt = 'http://www.omdbapi.com/?i={}&apikey={}'.format(imdb_id, app.config['OMDB_APIKEY'])
    response = requests.get(fmt)
    data = response.json()

    if data['Response'] == 'False':
        error = data['Error']

    return render_template('details.html', data=data, error=error)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/favourites')
@login_required
def favourites():
    favourites = []

    for favourite in Favourite.query.filter_by(user_id=current_user.username).all():
        fmt = 'http://www.omdbapi.com/?i={}&apikey={}'.format(favourite.imdbID, app.config['OMDB_APIKEY'])
        response = requests.get(fmt)
        data = response.json()
        if data['Response'] == 'True':
            favourites.append({
                    'Title': favourite.title,
                    'Poster': favourite.poster,
                    'imdbID': favourite.imdbID})

    return render_template('favourites.html', favourites=favourites)


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')



