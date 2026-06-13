from datetime import datetime
from app.extensions import db

class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)

    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(50), nullable=False)

    destination = db.Column(db.String(80), nullable=False)
    travel_date = db.Column(db.String(50), nullable=True)

    number_of_people = db.Column(db.Integer, nullable=False)
    number_of_nights = db.Column(db.Integer, nullable=False)

    special_requests = db.Column(db.Text, nullable=True)

    status = db.Column(db.String(20), default="pending")  

    created_at = db.Column(db.DateTime, default=datetime.utcnow)