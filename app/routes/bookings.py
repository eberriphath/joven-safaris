from flask import Blueprint, request, jsonify

from app.models.booking import Booking
from app.extensions import db
from app.utils.email import send_booking_notification


bookings_bp = Blueprint(
    "bookings",
    __name__
)



@bookings_bp.route("/book", methods=["POST"])
def create_booking():

    data = request.get_json()



    # =========================
    # REQUIRED FIELDS
    # =========================

    required_fields = [

        "full_name",
        "email",
        "phone",
        "passport_number"
        "destination",
        "number_of_nights"

    ]



    for field in required_fields:

        if not data.get(field):

            return jsonify({

                "error": f"{field} is required"

            }), 400




    try:


        # =========================
        # CREATE BOOKING
        # =========================

        booking = Booking(



            # PERSONAL INFORMATION

            full_name=data["full_name"],

            email=data["email"],

            phone=data["phone"],

            passport_number=data.get(
                "passport_number"
            ),

            date_of_birth=data.get(
                "date_of_birth"
            ),

            country_of_origin=data.get(
                "country_of_origin"
            ),




            # TRAVEL INFORMATION

            destination=data["destination"],

            travel_date=data.get(
                "travel_date"
            ),

            expected_travel_time=data.get(
                "expected_travel_time"
            ),

            number_of_nights=data["number_of_nights"],

            accommodation_preference=data.get(
                "accommodation_preference"
            ),




            # TRAVELLER INFORMATION

            resident_adults=data.get(
                "resident_adults",
                0
            ),

            resident_children=data.get(
                "resident_children",
                0
            ),

            non_resident_adults=data.get(
                "non_resident_adults",
                0
            ),

            non_resident_children=data.get(
                "non_resident_children",
                0
            ),




            # EMERGENCY CONTACT

            emergency_contact_name=data.get(
                "emergency_contact_name"
            ),

            emergency_contact_phone=data.get(
                "emergency_contact_phone"
            ),

            emergency_contact_relationship=data.get(
                "emergency_contact_relationship"
            ),




            # ADDITIONAL

            special_requests=data.get(
                "special_requests"
            )

        )




        # =========================
        # SAVE BOOKING
        # =========================

        db.session.add(booking)

        db.session.commit()




        send_booking_notification(
            booking
        )




        return jsonify({

            "message":
            "Booking received successfully",

            "booking_id":
            booking.id

        }), 201





    except Exception as e:


        db.session.rollback()


        return jsonify({

            "error": str(e)

        }), 500