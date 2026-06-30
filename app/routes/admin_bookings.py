from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.booking import Booking

admin_bookings_bp = Blueprint("admin_bookings", __name__)

ALLOWED_STATUSES = {
    "pending",
    "confirmed",
    "completed",
    "cancelled",
}

@admin_bookings_bp.route("/admin/bookings", methods=["GET"])
def get_all_bookings():

    bookings = Booking.query.order_by(
        Booking.created_at.desc()
    ).all()

    return jsonify([{
            "id": booking.id,
            "full_name": booking.full_name,
            "email": booking.email,
            "phone": booking.phone,
            "destination": booking.destination,
            "travel_date": booking.travel_date,
            "number_of_people": booking.number_of_people,
            "number_of_nights": booking.number_of_nights,
            "special_requests": booking.special_requests,
            "status": booking.status,
            "created_at": booking.created_at
            }
            for booking in bookings
    ])

@admin_bookings_bp.route("/admin/bookings/<int:booking_id>/status", methods=["PUT"])
def update_booking_status(booking_id):

    booking = Booking.query.get_or_404(booking_id)

    data = request.get_json()
    status = data.get("status")

    if status not in ALLOWED_STATUSES:
        return jsonify({
            "error":"invalid status"
        }),400

    booking.status = status

    db.session.commit()

    return jsonify({
        "message": "Booking status updated successfully",
        "booking_id": booking.id,
        "status": booking.status
    })