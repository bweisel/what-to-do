import datetime as dt

from whattodo.extensions import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.Binary(128), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    last_updated = db.Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %s>' % self.email
