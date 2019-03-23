import datetime

from werkzeug.security import generate_password_hash

from .base import BaseMixin, db


class User(BaseMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    passport_photo_url = db.Column(db.String(255), nullable=True)
    role = db.Column(db.Boolean, default=False)
    created_on = db.Column(db.DateTime, default=datetime.datetime.now, nullable=False)
    updated_on = db.Column(db.DateTime, default=datetime.datetime.now,
                           onupdate=datetime.datetime.now, nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password, method='sha256')
    
    def __repr__(self):
        return "<User :{}>".format(self.name)
