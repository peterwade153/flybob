import json

from flask import request, jsonify
from flask.views import MethodView

from app.models.flights import Flight
from utils.auth_token import token_required, admin_required


class RegisterFlightView(MethodView):
    """
    Admins register flights
    params:name, origin, destination, departure, arrive, duration, status, aircraft, capacity
    """

    decorators = [token_required, admin_required]

    def post(self, current_user):

        data = request.get_json()
        name = data.get('name')
        origin = data.get('origin')
        aircraft = data.get('aircraft')
        destination = data.get('destination')
        departure = data.get('departure')
        arrive = data.get('arrive')
        capacity = data.get('capacity')
        duration  = data.get('duration')
        status = data.get('status')

        if not all([name, origin, destination, departure, arrive, duration, status, aircraft, capacity]):
            return jsonify({
                'message' : 'All fields name, origin, destination,' 
                'departure, arrive, duration, status',
                'status': 'Failed'
            }), 400

        try:
            new_flight = Flight(name=name, origin=origin, destination=destination, 
                          departure=departure, arrive=arrive, duration=duration, capacity=capacity,
                          aircraft=aircraft, status=status, created_by=current_user)
            new_flight.save()
            return jsonify({
                'message':'Flight '+name+' to '+destination+' registered.',
                'status':' Success'
                }), 201
        except:
            return jsonify({
                'message': 'Regstration failed, please try again.'
            }), 400


class UpdateDeleteFlightView(MethodView):
    """
    Admin update flight data
    params: name, origin, destination, departure, arrive, duration, status, aircraft, capacity
    """
    decorators = [token_required, admin_required]

    def put(self, current_user, id):

        data = request.get_json()
        flight = Flight.get_by(id=id)
        if not flight:
            return jsonify({
                'message':"Flight not found",
                'status':'Failed'
            }), 404
        fields = ['name', 'origin', 'destination', 'departure', 'arrive', 'duration', 'status', 'aircraft', 'capacity']
        for field in data.keys():
            if field not in fields:
                return jsonify({
                    'message':" Unknown fields passed",
                    'status':"Failed"
                }), 400
        try:
            for attr, value in data.items():
                setattr(flight, attr, value)
                flight.save()
            return jsonify({
                'message':'Flight updated',
                'status':'Success'
            }), 200
        except:
            return jsonify({
                'message': "Flight update failed, please try again!",
                'status':"Failed"
            }),400
        
    def delete(self, current_user, id):

        flight = Flight.get_by(id=id)
        if not flight:
            return jsonify({
                'message':"Flight not found",
                'status':'Failed'
            }), 404
        try:
            flight.delete()
            return jsonify({
                'message':'Flight deleted',
                'status':'Success'
            }), 200
        except:
            return jsonify({
                'message': "Flight delete failed, please try again!",
                'status':"Failed"
            }),400


class GetAllFlights(MethodView):
    """
    Fetch all
    params:
    """
    decorators = [token_required]

    def get(self, current_user):
        flights = Flight.get_all()
        return jsonify({
            'flights':[flight.serialized_flight() for flight in flights],
            'status': 'Success'
        }), 200


class GetFlight(MethodView):
    """
    Fetch all
    params:
    """
    decorators = [token_required]

    def get(self, current_user, id):
        flight = Flight.get_by(id=id)
        return jsonify({
            'flights':flight.serialized_flight(),
            'status': 'Success'
        }), 200
