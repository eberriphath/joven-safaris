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



def send_car_rental_notification(rental):

    msg = Message(
        subject="New Car Rental Request",
        recipients=[ADMIN_EMAIL]
    )


    msg.body = f"""

================================
NEW CAR RENTAL REQUEST
================================


REQUEST DATE
------------
{rental.created_at.strftime("%Y-%m-%d %H:%M")}



CUSTOMER INFORMATION
--------------------

Full Name:
{rental.full_name}

Email:
{rental.email}

Phone:
{rental.phone}



RENTAL INFORMATION
------------------

Vehicle Type:
{rental.vehicle_type}

Pickup Location:
{rental.pickup_location}

Pickup Date:
{rental.pickup_date}

Pickup Time:
{rental.pickup_time}

Drop-off Location:
{rental.dropoff_location}

Drop-off Date:
{rental.dropoff_date}

Drop-off Time:
{rental.dropoff_time}



DRIVER INFORMATION
------------------

Driver Age:
{rental.driver_age or "Not provided"}

Driving License Number:
{rental.driving_license_number or "Not provided"}

License Country:
{rental.license_country or "Not provided"}



SPECIAL REQUESTS
----------------

{rental.special_requests or "None"}



STATUS
------

{rental.status}



================================
END OF CAR RENTAL REQUEST
================================

"""

    mail.send(msg)



def send_car_rental_confirmation_email(rental):

    msg = Message(
        subject="Thank You for Your Car Rental Request | Joven Safaris",
        recipients=[rental.email]
    )


    msg.body = f"""

Hello {rental.full_name},


Thank you for choosing Joven Safaris for your car rental needs.


We have successfully received your car rental request and
our team is now reviewing the details you provided.


CAR RENTAL REQUEST
------------------

Vehicle Type:
{rental.vehicle_type}

Pickup Location:
{rental.pickup_location}

Pickup Date:
{rental.pickup_date}

Pickup Time:
{rental.pickup_time}

Drop-off Location:
{rental.dropoff_location}

Drop-off Date:
{rental.dropoff_date}

Drop-off Time:
{rental.dropoff_time}


Your rental request has been received successfully.

A member of the Joven Safaris team will review your request
and contact you regarding availability, pricing, and the
next steps for your rental.


Please note that submitting this request does not yet
constitute a confirmed vehicle reservation.


If you have any questions or need to make changes to your
request, please feel free to contact us.


We look forward to helping make your journey easier.


Warm regards,

Joven Safaris
"""
    
    mail.send(msg)