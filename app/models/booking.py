from datetime import datetime
from app.extensions import db
from app.constants.statuses import BOOKING_STATUSES


class Booking(db.Model):

    __tablename__ = "bookings"



    id = db.Column(
        db.Integer,
        primary_key=True
    )



    full_name = db.Column(
        db.String(120),
        nullable=False
    )


    email = db.Column(
        db.String(120),
        nullable=False
    )


    phone = db.Column(
        db.String(50),
        nullable=False
    )


    passport_number = db.Column(
        db.String(100),
        nullable=True
    )


    date_of_birth = db.Column(
        db.String(50),
        nullable=True
    )


    country_of_origin = db.Column(
        db.String(100),
        nullable=True
    )




    destination = db.Column(
        db.String(120),
        nullable=False
    )


    travel_date = db.Column(
        db.String(50),
        nullable=True
    )


    expected_travel_time = db.Column(
        db.String(50),
        nullable=True
    )


    number_of_nights = db.Column(
        db.Integer,
        nullable=False
    )


    accommodation_preference = db.Column(
        db.String(100),
        nullable=True
    )




    resident_adults = db.Column(
        db.Integer,
        default=0
    )


    resident_children = db.Column(
        db.Integer,
        default=0
    )


    non_resident_adults = db.Column(
        db.Integer,
        default=0
    )


    non_resident_children = db.Column(
        db.Integer,
        default=0
    )




    emergency_contact_name = db.Column(
        db.String(120),
        nullable=True
    )


    emergency_contact_phone = db.Column(
        db.String(50),
        nullable=True
    )


    emergency_contact_relationship = db.Column(
        db.String(50),
        nullable=True
    )




    special_requests = db.Column(
        db.Text,
        nullable=True
    )




    status = db.Column(
        db.String(20),
        default="pending",
        nullable=False
    )


    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )