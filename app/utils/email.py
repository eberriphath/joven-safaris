import os
from flask_mail import Message
from app.extensions import mail

ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")

def send_booking_notification(booking):

    msg = Message(
        subject="New Booking",
        recipients=[ADMIN_EMAIL]
    )
    msg.body = f"""
New booking received

Name: {booking.full_name}
Email: {booking.email}
Phone: {booking.phone}

Destination: {booking.destination}
People: {booking.number_of_people}
Nights: {booking.number_of_nights}

{booking.special_requests or "No special requests"}

{booking.status}

{booking.created_at}
"""
    mail.send(msg)
