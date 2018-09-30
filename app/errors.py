from flask import flash, redirect, url_for

from app import app, db


@app.errorhandler(401)
def custom_401(error):
    flash('Unauthorized access. Please login')
    return redirect(url_for('index'))


@app.errorhandler(404)
def _404(error):
    flash('Page not found')
    return redirect(url_for('index'))


