from flask import Blueprint, jsonify
from app.utils.auth import admin_required
from app.models.booking import Booking
from app.models.car_rental import CarRental


admin_dashboard_bp = Blueprint(
    "admin_dashboard",
    __name__
)


@admin_dashboard_bp.route(
    "/admin/dashboard",
    methods=["GET"]
)
@admin_required
def dashboard():

    # ==========================================
    # SAFARI BOOKING STATISTICS
    # ==========================================

    total = Booking.query.count()

    pending = Booking.query.filter_by(
        status="pending"
    ).count()

    confirmed = Booking.query.filter_by(
        status="confirmed"
    ).count()

    cancelled = Booking.query.filter_by(
        status="cancelled"
    ).count()

    completed = Booking.query.filter_by(
        status="completed"
    ).count()


    # ==========================================
    # CAR RENTAL STATISTICS
    # ==========================================

    total_car_rentals = CarRental.query.count()


    # ==========================================
    # RECENT BOOKINGS
    # ==========================================

    recent_bookings = (
        Booking.query
        .order_by(
            Booking.created_at.desc()
        )
        .limit(5)
        .all()
    )


    # ==========================================
    # RESPONSE
    # ==========================================

    return jsonify({

        "total_bookings": total,

        "pending": pending,

        "confirmed": confirmed,

        "cancelled": cancelled,

        "completed": completed,

        "total_car_rentals":
            total_car_rentals,


        "recent_bookings": [

            {
                "id": booking.id,

                "full_name":
                    booking.full_name,

                "destination":
                    booking.destination,

                "status":
                    booking.status,

                "created_at":
                    booking.created_at

            }

            for booking in recent_bookings

        ]

    })