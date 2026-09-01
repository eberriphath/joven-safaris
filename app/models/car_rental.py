from datetime import datetime

from app.extensions import db
from app.constants.statuses import CAR_RENTAL_STATUSES


class CarRental(db.Model):

    __tablename__ = "car_rentals"


    id = db.Column(
        db.Integer,
        primary_key=True
    )


    # =========================
    # CUSTOMER INFORMATION
    # =========================

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


    # =========================
    # RENTAL INFORMATION
    # =========================

    vehicle_type = db.Column(
        db.String(120),
        nullable=False
    )


    pickup_location = db.Column(
        db.String(150),
        nullable=False
    )


    dropoff_location = db.Column(
        db.String(150),
        nullable=False
    )


    pickup_date = db.Column(
        db.String(50),
        nullable=False
    )


    pickup_time = db.Column(
        db.String(50),
        nullable=False
    )


    dropoff_date = db.Column(
        db.String(50),
        nullable=False
    )


    dropoff_time = db.Column(
        db.String(50),
        nullable=False
    )


    # =========================
    # DRIVER INFORMATION
    # =========================

    driver_age = db.Column(
        db.Integer,
        nullable=True
    )


    driving_license_number = db.Column(
        db.String(100),
        nullable=True
    )


    license_country = db.Column(
        db.String(100),
        nullable=True
    )


    # =========================
    # ADDITIONAL INFORMATION
    # =========================

    special_requests = db.Column(
        db.Text,
        nullable=True
    )


    # =========================
    # STATUS
    # =========================

    status = db.Column(
        db.String(20),
        default="pending",
        nullable=False
    )


    # =========================
    # TIMESTAMP
    # =========================

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )