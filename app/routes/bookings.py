from flask import Blueprint, request, jsonify
from app.models.booking import Booking
from app.extensions import db

bookings_bp = Blueprint("bookings", __name__)

@bookings_bp.route("/book", methods=["POST"])
def create_booking():
    data = request.get_json()

    required_fields = ["full_name", "email", "phone", "destination", "number_of_people", "number_of_nights"]
    for field in required_fields:
        if not data.get(field):
            return jsonify({"error": f"{field} is required"}), 400

    booking = Booking(
        full_name=data["full_name"],
        email=data["email"],
        phone=data["phone"],
        destination=data["destination"],
        travel_date=data.get("travel_date"),
        number_of_people=data["number_of_people"],
        number_of_nights=data["number_of_nights"],
        special_requests=data.get("special requests")
    )

    db.session.add(booking)
    db.session.commit()
    return jsonify({
        "message": "Booking received successfully",
        "booking_id": booking.id
    }), 201
