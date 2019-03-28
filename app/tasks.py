from datetime import date, timedelta

from flask_mail import Message
from sqlalchemy import func

from app import celery, mail
from app.models.reservations import Reservation
from app.models.flights import Flight


@celery.task
def flight_reminder():
    #filter out flihghts for the following day.
    departure = (date.today()+timedelta(days=1)).strftime("%Y-%m-%d")
    tomorrow_flights = Reservation.query.join(Flight).filter(func.date(Flight.departure)==departure)

    for i in tomorrow_flights:
        user = i.user
        flight = i.flight
        msg = Message(subject = "Reminder about flight"+str(flight.name),
                      body = "Hello "+user.name+" This is to remind you that flight "+flight.name+" you booked is on tomorrow",
                      recipients=[user.email],
                      )
        mail.send(msg)
