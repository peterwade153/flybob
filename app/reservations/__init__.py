from flask import Blueprint

from app.reservations.views import ReservationsView, ReservationGetUpdateView


reservations_blueprint = Blueprint(
    "reservations", __name__, url_prefix=("/api/v1")
)

make_reservations = ReservationsView.as_view("reservations")
reservations_blueprint.add_url_rule(
    "/reservations", view_func=make_reservations, methods=["POST", "GET"]
)

update_get_reservations = ReservationGetUpdateView.as_view(
    "update_reservations"
)
reservations_blueprint.add_url_rule(
    "/reservations/<id>",
    view_func=update_get_reservations,
    methods=["GET", "PUT"],
)
