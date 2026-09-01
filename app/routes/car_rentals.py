from flask import Blueprint, request, jsonify

from app.models.car_rental import CarRental
from app.extensions import db
from app.utils.email import (
    send_car_rental_notification,
    send_car_rental_confirmation_email
)


car_rentals_bp = Blueprint(
    "car_rentals",
    __name__
)


@car_rentals_bp.route(
    "/car-rentals",
    methods=["POST"]
)
def create_car_rental():

    data = request.get_json()


    if not data:

        return jsonify({
            "error": "Request data is required"
        }), 400


    # =========================
    # REQUIRED FIELDS
    # =========================

    required_fields = [

        "full_name",
        "email",
        "phone",

        "vehicle_type",

        "pickup_location",
        "dropoff_location",

        "pickup_date",
        "pickup_time",

        "dropoff_date",
        "dropoff_time"

    ]


    for field in required_fields:

        if not data.get(field):

            return jsonify({

                "error":
                f"{field} is required"

            }), 400


    try:

        # =========================
        # CREATE RENTAL
        # =========================

        rental = CarRental(

            # CUSTOMER

            full_name=data["full_name"],

            email=data["email"],

            phone=data["phone"],


            # RENTAL

            vehicle_type=data["vehicle_type"],

            pickup_location=data["pickup_location"],

            dropoff_location=data["dropoff_location"],

            pickup_date=data["pickup_date"],

            pickup_time=data["pickup_time"],

            dropoff_date=data["dropoff_date"],

            dropoff_time=data["dropoff_time"],


            # DRIVER

            driver_age=data.get(
                "driver_age"
            ),

            driving_license_number=data.get(
                "driving_license_number"
            ),

            license_country=data.get(
                "license_country"
            ),


            # ADDITIONAL

            special_requests=data.get(
                "special_requests"
            )

        )


        # =========================
        # SAVE
        # =========================

        db.session.add(rental)

        db.session.commit()


        # =========================
        # SEND EMAILS
        # =========================

        send_car_rental_notification(
            rental
        )


        send_car_rental_confirmation_email(
            rental
        )


        # =========================
        # RESPONSE
        # =========================

        return jsonify({

            "message":
            "Car rental request received successfully",

            "rental_id":
            rental.id

        }), 201


    except Exception as e:

        db.session.rollback()


        return jsonify({

            "error": str(e)

        }), 500