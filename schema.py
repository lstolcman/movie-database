import app
from app import db
from app.models import User, Favourite
from werkzeug.security import generate_password_hash


db.create_all()

u1 = User(username='1', email='e.m@i.l1', password_hash=generate_password_hash('1'))
u2 = User(username='2', email='e.m@i.l2', password_hash=generate_password_hash('2'))
u3 = User(username='3', email='e.m@i.l3', password_hash=generate_password_hash('3'))
db.session.add(u1)
db.session.add(u2)
db.session.add(u3)
db.session.commit()

f1 = Favourite(user=u1, movie_id='tt2653342')
f2 = Favourite(user=u1, movie_id='tt6172126')
db.session.add(f1)
db.session.add(f2)
f3 = Favourite(user=u2, movie_id='tt4011326')
f4 = Favourite(user=u2, movie_id='tt6172126')
db.session.add(f3)
db.session.add(f4)
db.session.commit()

User.query.all()

