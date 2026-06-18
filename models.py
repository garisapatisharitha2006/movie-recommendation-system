from extensions import db
from flask_login import UserMixin

watchlist = db.Table(
    'watchlist',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id'))
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    preferred_language = db.Column(db.String(50))
    preferred_genre = db.Column(db.String(50))

    movies = db.relationship('Movie', secondary=watchlist)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    genre = db.Column(db.String(100))
    language = db.Column(db.String(50))
    rating = db.Column(db.Float)
    image = db.Column(db.String(200))