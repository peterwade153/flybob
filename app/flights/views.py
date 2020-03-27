import json

from flask import request, jsonify
from flask.views import MethodView

from app.models.flights import Flight
from app.flights.flight_utils import check_all_fields_flight_register, check_flight_fields_update
from utils.auth_token import token_required, admin_required


class RegisterFlightView(MethodView):
    """
    Admins register flights
    params:name, origin, destination, departure, arrive, duration, status, aircraft, capacity
    """

    decorators = [token_required, admin_required]

    def post(self, current_user):

        data = request.get_json()

        fields_res = check_all_fields_flight_register(data)
        if fields_res:
            return fields_res

        new_flight = Flight(
            name=data.get("name"),
            origin=data.get("origin"),
            destination=data.get("destination"),
            departure=data.get("departure"),
            arrive=data.get("arrive"),
            duration=data.get("duration"),
            capacity=data.get("capacity"),
            aircraft=data.get("aircraft"),
            status=data.get("status"),
            created_by=current_user,
        )
        new_flight.save()
        return (
            jsonify(
                {
                    "message": "Flight "
                    + data.get("name")
                    + " to "
                    + data.get("destination")
                    + " registered.",
                    "status": " Success",
                }
            ),
            201,
        )


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
            return (
                jsonify({"message": "Flight not found", "status": "Failed"}),
                404,
            )
        fields_res = check_flight_fields_update(data)
        if fields_res:
            return fields_res

        # update
        for attr, value in data.items():
            setattr(flight, attr, value)
            flight.save()
        return jsonify({"message": "Flight updated", "status": "Success"}), 200

    def delete(self, current_user, id):

        flight = Flight.get_by(id=id)
        if not flight:
            return (
                jsonify({"message": "Flight not found", "status": "Failed"}),
                404,
            )

        flight.delete()
        return jsonify({"message": "Flight deleted", "status": "Success"}), 200


class GetAllFlights(MethodView):
    """
    Fetch all flights
    params:
    """

    decorators = [token_required]

    def get(self, current_user):
        flights = Flight.get_all()
        return (
            jsonify(
                {
                    "flights": [
                        flight.serialized_flight() for flight in flights
                    ],
                    "status": "Success",
                }
            ),
            200,
        )


class GetFlight(MethodView):
    """
    Fetch a flight
    params: id
    """

    decorators = [token_required]

    def get(self, current_user, id):
        flight = Flight.get_by(id=id)
        return (
            jsonify(
                {"flights": flight.serialized_flight(), "status": "Success"}
            ),
            200,
        )
