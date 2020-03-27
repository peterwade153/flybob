from flask import jsonify

fields = ["name","origin","destination","departure","arrive","duration","status","aircraft","capacity"]

def check_all_fields_flight_register(data):
    """
    Returns an error if a required field is missing
    params:data
    """

    name = data.get("name")
    origin = data.get("origin")
    aircraft = data.get("aircraft")
    destination = data.get("destination")
    departure = data.get("departure")
    arrive = data.get("arrive")
    capacity = data.get("capacity")
    duration = data.get("duration")
    status = data.get("status")
    
    if not all(
        [
            name,
            origin,
            destination,
            departure,
            arrive,
            duration,
            status,
            aircraft,
            capacity,
        ]
    ):
        return (
            jsonify(
                {
                    "message": "All fields name, origin, destination,"
                    "departure, arrive, duration, status",
                    "status": "Failed",
                }
            ),
            400,
        )

def check_flight_fields_update(data):
    """
    Return as error if an incorrect fields passed in flight data
    params: data
    """
    
    for field in data.keys():
        if field not in fields:
            return (
                jsonify(
                    {
                        "message": " Unknown fields passed",
                        "status": "Failed",
                    }
                ),
                400,
            )