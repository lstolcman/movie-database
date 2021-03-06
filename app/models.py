from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

from app import db, login


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    favourites = db.relationship('Favourite', backref='user', lazy=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Favourite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    imdbID = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    poster = db.Column(db.String(150), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<Favourite {} of user {}>'.format(self.imdbID, self.user_id)

