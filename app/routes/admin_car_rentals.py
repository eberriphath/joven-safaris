from flask import Blueprint, request, jsonify

from app.extensions import db
from app.models.car_rental import CarRental
from app.utils.auth import admin_required


admin_car_rentals_bp = Blueprint(
    "admin_car_rentals",
    __name__
)


ALLOWED_STATUSES = {
    "pending",
    "confirmed",
    "completed",
    "rejected"
}


# ==========================================
# GET ALL CAR RENTALS
# ==========================================

@admin_car_rentals_bp.route(
    "/admin/car-rentals",
    methods=["GET"]
)
@admin_required
def get_all_car_rentals():

    rentals = CarRental.query.order_by(
        CarRental.created_at.desc()
    ).all()


    return jsonify([

        {
            "id": rental.id,

            # CUSTOMER
            "full_name": rental.full_name,
            "email": rental.email,
            "phone": rental.phone,

            # RENTAL
            "vehicle_type": rental.vehicle_type,

            "pickup_location":
                rental.pickup_location,

            "dropoff_location":
                rental.dropoff_location,

            "pickup_date":
                rental.pickup_date,

            "pickup_time":
                rental.pickup_time,

            "dropoff_date":
                rental.dropoff_date,

            "dropoff_time":
                rental.dropoff_time,

            # DRIVER
            "driver_age":
                rental.driver_age,

            "driving_license_number":
                rental.driving_license_number,

            "license_country":
                rental.license_country,

            # ADDITIONAL
            "special_requests":
                rental.special_requests,

            # STATUS
            "status":
                rental.status,

            # DATE
            "created_at":
                rental.created_at

        }

        for rental in rentals

    ])


# ==========================================
# UPDATE CAR RENTAL STATUS
# ==========================================

@admin_car_rentals_bp.route(
    "/admin/car-rentals/<int:rental_id>/status",
    methods=["PUT"]
)
@admin_required
def update_car_rental_status(rental_id):

    rental = CarRental.query.get_or_404(
        rental_id
    )


    data = request.get_json()


    if not data:

        return jsonify({
            "error": "Request data is required"
        }), 400


    status = data.get("status")


    if status not in ALLOWED_STATUSES:

        return jsonify({
            "error": "Invalid status"
        }), 400


    rental.status = status

    db.session.commit()


    return jsonify({

        "message":
            "Car rental status updated successfully",

        "rental_id":
            rental.id,

        "status":
            rental.status

    }), 200


# ==========================================
# DELETE CAR RENTAL
# ==========================================

@admin_car_rentals_bp.route(
    "/admin/car-rentals/<int:rental_id>",
    methods=["DELETE"]
)
@admin_required
def delete_car_rental(rental_id):

    rental = CarRental.query.get_or_404(
        rental_id
    )


    db.session.delete(rental)

    db.session.commit()


    return jsonify({

        "message":
            "Car rental deleted successfully"

    }), 200