import datetime

from .base import BaseMixin, db


class TokenBlacklist(BaseMixin, db.Model):
    """
    For storing Blacklisted tokens on user logout
    """
    __tablename__ = 'tokens_blacklist'

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(255), nullable=False)
    blacklisted_on = db.Column(db.DateTime, default=datetime.datetime.now, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()

    def __repr__(self):
        return "<token :{}>".format(self.token)
