from flask import Blueprint

from app.flights.views import RegisterFlightView, UpdateDeleteFlightView, GetAllFlights, GetFlight

flight_blueprint = Blueprint('flight', __name__, url_prefix='/api/v1')

register_flight = RegisterFlightView.as_view('flights')
flight_blueprint.add_url_rule('/flights',
                              view_func=register_flight,
                              methods =['POST'] )

update_delete_flight = UpdateDeleteFlightView.as_view('update_flights')
flight_blueprint.add_url_rule('/flights/<id>',
                              view_func=update_delete_flight,
                              methods =['PUT', 'DELETE'] )

get_all_flights = GetAllFlights.as_view('all_flights')
flight_blueprint.add_url_rule('/flights',
                              view_func=get_all_flights,
                              methods=['GET'])

get_flight = GetFlight.as_view('flight')
flight_blueprint.add_url_rule('/flights/<id>',
                              view_func=get_flight,
                              methods=['GET'])
