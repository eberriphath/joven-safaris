import os

from flask_mail import Message
from app.extensions import mail


ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")



def send_booking_notification(booking):


    msg = Message(

        subject="New Safari Booking Request",

        recipients=[ADMIN_EMAIL]

    )



    msg.body = f"""

================================
NEW SAFARI BOOKING REQUEST
================================


BOOKING DATE
------------
{booking.created_at.strftime("%Y-%m-%d %H:%M")}



PERSONAL INFORMATION
--------------------

Full Name:
{booking.full_name}

Email:
{booking.email}

Phone:
{booking.phone}

Passport / ID Number:
{booking.passport_number}

Date of Birth:
{booking.date_of_birth}

Country of Origin:
{booking.country_of_origin}



TRAVEL INFORMATION
------------------

Destination:
{booking.destination}

Travel Date:
{booking.travel_date}

Expected Travel Time:
{booking.expected_travel_time}

Number of Nights:
{booking.number_of_nights}

Accommodation Preference:
{booking.accommodation_preference}



TRAVELLER INFORMATION
---------------------

Resident Adults:
{booking.resident_adults}

Resident Children:
{booking.resident_children}

Non-Resident Adults:
{booking.non_resident_adults}

Non-Resident Children:
{booking.non_resident_children}



EMERGENCY CONTACT
-----------------

Name:
{booking.emergency_contact_name}

Phone:
{booking.emergency_contact_phone}

Relationship:
{booking.emergency_contact_relationship}



SPECIAL REQUESTS
----------------

{booking.special_requests or "None"}



================================
END OF BOOKING REQUEST
================================

"""


    mail.send(msg)