import datetime as dt

from whattodo.extensions import db


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    created = db.Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    last_updated = db.Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)

    user = db.relationship('User', backref='items')

    def __init__(self, description, user_id):
        self.description = description
        self.user_id = user_id

    def __repr__(self):
        return '<Item %s>' % self.description
