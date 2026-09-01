import os

from flask_mail import Message
from app.extensions import mail


ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")


def send_booking_notification(booking):


    msg = Message(

        subject="New Safari Booking Request",

        recipients=[ADMIN_EMAIL]

    )


    # =========================
    # CHILDREN AGES
    # =========================

    resident_ages = (
        booking.resident_children_ages
        or []
    )

    non_resident_ages = (
        booking.non_resident_children_ages
        or []
    )


    # Format resident children ages

    if resident_ages:

        resident_children_ages_text = "\n".join(
            f"Child {index + 1}: {age} years"
            for index, age in enumerate(resident_ages)
        )

    else:

        resident_children_ages_text = "None"



    # Format non-resident children ages

    if non_resident_ages:

        non_resident_children_ages_text = "\n".join(
            f"Child {index + 1}: {age} years"
            for index, age in enumerate(non_resident_ages)
        )

    else:

        non_resident_children_ages_text = "None"



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

RESIDENTS
---------

Adults:
{booking.resident_adults}

Children:
{booking.resident_children}


Resident Children Ages:
{resident_children_ages_text}



NON-RESIDENTS
-------------

Adults:
{booking.non_resident_adults}

Children:
{booking.non_resident_children}


Non-Resident Children Ages:
{non_resident_children_ages_text}



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


def send_password_reset_email(email, token):

    reset_link = f"http://localhost:5173/reset-password/{token}"

    msg = Message(
        subject="Joven Safaris Admin Password Reset",
        recipients=[email]
    )

    msg.body = f"""
Hello,

We received a request to reset your Joven Safaris Admin password.

Click the link below to reset your password:

{reset_link}

This link will expire in 30 minutes.

If you did not request this password reset, simply ignore this email.

Regards,
Joven Safaris
"""

    mail.send(msg)




def send_booking_confirmation_email(booking):


    msg = Message(

        subject="Thank You for Booking with Joven Safaris",

        recipients=[booking.email]

    )


    msg.body = f"""

Hello {booking.full_name},


Thank you for choosing Joven Safaris.


We have successfully received your safari booking request and
our team is now reviewing the details you provided.


BOOKING DETAILS
---------------

Destination:
{booking.destination}

Travel Date:
{booking.travel_date}

Number of Nights:
{booking.number_of_nights}

Accommodation Preference:
{booking.accommodation_preference}


Your booking request has been received successfully.

A member of the Joven Safaris team will review your request and
contact you with the next steps and confirmation.


If you have any questions or need to make changes to your request,
please feel free to contact us.


We look forward to helping you experience an unforgettable safari.


Warm regards,

Joven Safaris
"""
    
    mail.send(msg)

