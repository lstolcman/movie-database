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
    pages = None


    fmt = 'http://www.omdbapi.com/?type=movie&s={}&page={}&apikey={}'.format(title, page, app.config['OMDB_APIKEY'])
    response = requests.get(fmt)
    data = response.json()

    if data['Response'] == 'False':
        flash(data['Error'])
    else:
        for i, v in enumerate(data['Search']):
            data['Search'][i]['user_fav'] = Favourite.query.filter_by(user_id=current_user.username, imdbID=data['Search'][i]['imdbID']).first()
            data['active_page'] = page
            data['pages'] = range(1, math.ceil(int(data['totalResults'])/10)+1)

    return render_template('search.html', data=data, title=title)


@app.route('/details/<imdb_id>')
@login_required
def details(imdb_id):
    user_fav = Favourite.query.filter_by(user_id=current_user.username, imdbID=imdb_id).first()

    fmt = 'http://www.omdbapi.com/?i={}&apikey={}'.format(imdb_id, app.config['OMDB_APIKEY'])
    response = requests.get(fmt)
    data = response.json()

    if data['Response'] == 'False':
        flash(data['Error'])
        return redirect(url_for('details'))

    return render_template('details.html', data=data, user_fav=user_fav)


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


@app.route('/favourites/<imdb_id>')
@app.route('/favourites/', defaults={'imdb_id':None})
@login_required
def favourites(imdb_id):
    user_fav = Favourite.query.filter_by(user_id=current_user.username, imdbID=imdb_id).first()
    if imdb_id:
        if user_fav:
            db.session.delete(user_fav)
            db.session.commit()
        else:
            fmt = 'http://www.omdbapi.com/?i={}&apikey={}'.format(imdb_id, app.config['OMDB_APIKEY'])
            response = requests.get(fmt)
            data = response.json()
            if data['Response'] == 'True':
                fav_new_item = Favourite(user=current_user, imdbID=imdb_id, title=data['Title'], poster=data['Poster'])
                db.session.add(fav_new_item)
                db.session.commit()
            else:
                flash('Cannot add to favourites')

    favourites = []

    favourities_db = Favourite.query.filter_by(user_id=current_user.username).all()
    for favourite in favourities_db:
        favourites.append({
            'Title': favourite.title,
            'Poster': favourite.poster,
            'imdbID': favourite.imdbID})

    return render_template('favourites.html', favourites=favourites, user_fav=user_fav)


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')



