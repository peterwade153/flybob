import datetime

from .base import BaseMixin, db


class Reservation(BaseMixin, db.Model):
    __tablename__ = "reservations"

    id = db.Column(db.Integer, primary_key=True)
    flight_id = db.Column(
        db.Integer, db.ForeignKey("flights.id"), nullable=False
    )
    flight = db.relationship(
        "Flight", backref=db.backref("reservations", lazy="dynamic")
    )
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", backref=db.backref("users", lazy="dynamic"))
    seats_booked = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    booked_on = db.Column(
        db.DateTime, default=datetime.datetime.now, nullable=False
    )
    updated_on = db.Column(
        db.DateTime,
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now,
        nullable=False,
    )

    def __init__(self, flight_id, user_id, seats_booked, status=True):
        self.flight_id = flight_id
        self.user_id = user_id
        self.seats_booked = seats_booked
        self.status = status

    def __repr__(self):
        return "<Reservation:{}>".format(self.id)

    def serialized_reservation(self):
        return {
            "id": self.id,
            "flight_id": self.flight_id,
            "flight": self.flight.name,
            "seats_booked": self.seats_booked,
            "status": self.status,
            "booked_on": self.booked_on,
        }
