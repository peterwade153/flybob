from flask import request, jsonify
from flask.views import MethodView
from sqlalchemy import func

from app.models.reservations import Reservation
from app.models.flights import Flight
from app.models.base import db
from utils.auth_token import token_required


class ReservationsView(MethodView):
    """
    Enable users book flights and view all booked flights
    params: flight_id, seats_booked
    """
    decorators = [token_required]

    def post(self, current_user):

        data = request.get_json()
        flight_id = data.get('flight_id')
        seats_booked = data.get('seats_booked')

        if not all([flight_id, seats_booked]):
            return jsonify({
                'message' : 'Flight ID and Seats booked are required',
                'status' : 'Failed'
            }), 400
        flight = Flight.get_by(id = flight_id)
        if not flight:
            return jsonify({
                'message':"Flight not found",
                'status':'Failed'
            }), 404
        
        try:
            if seats_booked > flight.capacity:
                return jsonify({
                    'message': 'Current seating capacity is '+str(flight.capacity),
                    'status':'Failed'
                }), 202
            #update the flight capacity
            new_flight_capacity = flight.capacity - int(seats_booked)
            flight.update(capacity=new_flight_capacity)

            book = Reservation(flight_id=flight_id, seats_booked=seats_booked, user_id=current_user)
            book.save()

            return jsonify({
                'message':'Reservation on '+flight.name+' made successfully!',
                'status' : 'Success'
            }), 201
        except:
            return jsonify({
                'message': "Flight reservation failed, please try again!",
                'status':"Failed"
            }),400
    
    def get(self, current_user):

        flight = request.args.get('flight', None)
        booked_on = request.args.get('booked_on', None)
        if flight and booked_on:
            seats_booked = 0
            booked_flights = Reservation.query.join(Flight).filter(func.date(Reservation.booked_on)==booked_on, 
                                                                   Flight.name==flight)
            for b in booked_flights:
                seats_booked =+b.seats_booked 
            return jsonify({
                'seats_booked': seats_booked,
                'reservations':booked_flights.count()
            }), 200
        
        reservations = Reservation.get_all()
        return jsonify({
            'reservations' : [reservation.serialized_reservation() for reservation in reservations],
            'status':'Success'
        }), 200


class ReservationGetUpdateView(MethodView):
    """
    Update and Return a reservation
    params: flight_id
    """
    decorators = [token_required]

    def put(self, current_user, id):

        data = request.get_json()
        reservation = Reservation.get_by(id=id)
        if not reservation:
            return jsonify({
                'message':"Reservation not found",
                'status':'Failed'
            }), 404
        fields = ['seats_booked', 'status']
        for field in data.keys():
            if field not in fields:
                return jsonify({
                    'message':" Unknown fields passed",
                    'status':"Failed"
                }), 400
        try:
            for attr, value in data.items():
                setattr(reservation, attr, value)
                reservation.save()
            return jsonify({
                'message' : 'Reservation updated',
                'status' : 'Success'
            }), 200
        except:
            return jsonify({
                'message': "Reservation update failed, please try again!",
                'status':"Failed"
            }),400
    
    def get(self, current_user, id):

        reservation = Reservation.get_by(id=id)
        if not reservation:
            return jsonify({
                'message':"Reservation not found",
                'status':'Failed'
            }), 404

        return jsonify({
            'reservation':reservation.serialized_reservation(),
            'status':'Success'
        }), 200
