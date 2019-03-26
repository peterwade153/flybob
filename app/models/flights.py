import datetime

from .base import BaseMixin, db


class Flight(BaseMixin, db.Model):
    __tablename__ = 'flights'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    origin = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    departure = db.Column(db.DateTime, nullable=False)
    arrive = db.Column(db.DateTime, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    aircraft = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(100), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.datetime.now, nullable=False)
    updated_on = db.Column(db.DateTime, default=datetime.datetime.now,
                           onupdate=datetime.datetime.now, nullable=False)

    def __init__(self, name, origin, destination, departure, capacity, arrive, aircraft, duration, status, created_by):
        self.name = name
        self.origin = origin
        self.destination = destination
        self.departure = departure
        self.arrive = arrive
        self.aircraft = aircraft
        self.capacity = capacity
        self.duration = duration
        self.status = status
        self.created_by = created_by
    
    def __repr__(self):
        return "<User :{}>".format(self.name)

    def serialized_flight(self):
        return {'id':self.id,
                'name': self.name, 
                'origin': self.origin, 
                'destination':self.destination,
                'departure': self.departure, 
                'arrive': self.arrive,
                'capacity': self.capacity, 
                'duration':self.duration, 
                'status':self.status, 
                'aircraft':self.aircraft,
                'created_by':self.created_by,
                'created_on':self.created_on
            }
