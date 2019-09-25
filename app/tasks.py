from datetime import date, timedelta

from sqlalchemy import func
import celery

from app import app
from app.models.reservations import Reservation
from app.models.flights import Flight
from app.emails import mail_send


@celery.task
def flight_reminder():
    with app.app_context():
        # filter out flights for the following day.
        departure = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")
        tomorrow_flights = Reservation.query.join(Flight).filter(
            func.date(Flight.departure) == departure
        )

        for booking in tomorrow_flights:

            user = booking.user
            flight = booking.flight
            mail_send(
                subject="Reminder about flight " + str(flight.name),
                recipients=[user.email],
                text_body="Hello "
                + user.username
                + " This is to remind you that flight "
                + flight.name
                + " you booked, will be departing tomorrow for "
                + flight.destination
                + ".",
            )
