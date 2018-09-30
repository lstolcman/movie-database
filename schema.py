import app
from app import db
from app.models import User, Favourite
from werkzeug.security import generate_password_hash


db.create_all()

u = User(username='2', email='e.m@i.l', password_hash=generate_password_hash('2'))
db.session.add(u)
db.session.commit()

User.query.all()

