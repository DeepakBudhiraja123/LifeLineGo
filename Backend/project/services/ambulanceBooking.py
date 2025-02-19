from flask_smorest import abort
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from flask import current_app

from datetime import datetime, timedelta
import random

from project.db import db

from project.tables import HospitalModel, BookingRequestModel,BookingModel,UserModel, OTPModel
from project.schemas import OrderRequestSchema, BookingSchema
from project.services.helper import manage_address_field
from project.services.tasks import send_email

from project.scheduler import scheduler
from project.mail_config import mail

from flask_mail import Message






def create_order_request(request_data, user_id):
    """Create a new ambulance booking request"""

    # Check if hospital exists
    hospital = HospitalModel.query.get(request_data["hospital_id"])
    if not hospital:
        abort(404, message="Hospital not found.")
    field = manage_address_field(request_data)
    
    # Create new order request
    order_request = BookingRequestModel(
        name=request_data["name"],
        age=request_data["age"],
        sex=request_data["sex"],
        user_id=user_id,
        hospital_id=request_data["hospital_id"],
        ambulance_type=request_data["ambulance_type"],
        status="pending",
        created_at=datetime.utcnow(),
        **field
    )

    # Save to DB
    try:
        db.session.add(order_request)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        abort(400, message="Invalid data.")
    except Exception as e:
        print("Exception:", str(e))
        db.session.rollback()
        abort(500, message="An error occurred while saving the order request.")
        
    # Send email to the hospital
    try:
        email_body = f"""
        Dear {hospital.name},

        You have received a new ambulance booking request.

        Patient Name: {request_data["name"]}
        Age: {request_data["age"]}
        Sex: {request_data["sex"]}
        Ambulance Type: {request_data["ambulance_type"]}
        Pickup Address: {field["street"]}, {field['city_state'].city}, {field["city_state"].state}, {field['city_state'].postal_code}

        Please check your dashboard for more details.

        Best Regards,
        LifeLineGo Team
        """
        task = send_email.delay({"to_email":f"{hospital.email}", "subject":"New Ambulance Booking Request", "body":email_body})
    except Exception as e:
        current_app.logger.error(f"Failed to send email: {str(e)}")
    
    # Schedule the auto-reject job synchronously with a reason
    scheduler.add_job(
        func=auto_reject_booking,
        trigger="date",
        run_date=datetime.utcnow() + timedelta(minutes=15),
        args=[current_app._get_current_object(), order_request.id, "Hospital did not respond in time"],
        id=f"auto_reject_{order_request.id}",
        replace_existing=True,
    )


    # Return response with patient details
    return {
        "message": "Order request created successfully.",
        "data": {
            "order_request": order_request.to_dict(),
            "patient_details":{
                "patientName": request_data["name"],
                "patientAge": request_data["age"],
                "patientSex": request_data["sex"],
            }
        },
        "status": 201
    }, 201




def respond_to_booking(data,booking_id,hospital_id):
    """Step 1: Hospital responds with accepted/rejected."""
    if "status" not in data:
        abort(400, message="Missing status field.")
        
    if not isinstance(data.get("status"), str):
        abort(400, message="Invalid status.")
    status = data.get("status")

    if status not in ["accepted", "rejected"]:
      abort(400, message="Invalid status. Use 'accepted' or 'rejected'.")

    booking = BookingRequestModel.query.get(booking_id)
    if not booking:
        abort(404, message="Booking request not found.")

    if booking.status != "pending":
        abort(400, message="Booking has already been processed.")
    if str(booking.hospital_id) != hospital_id:
        abort(403, message="Access forbidden: Booking request not for this hospital.")
        
    if status == "rejected":
        if "reason" not in data:
            abort(400, message = "Reason must be specified while rejecting the request")
            
        reason = data.get("reason")
        if not isinstance(reason, str):
            abort(400, message="Invalid reason.")
        booking.reason_of_rejection = reason

    booking.status = status
    booking.updated_at = datetime.utcnow() # Update timestamp

    db.session.commit()
    
    # Remove previous auto-reject job if hospital responded
    job_id = f"auto_reject_{booking_id}"
    job = scheduler.get_job(job_id)
    if job:
        scheduler.remove_job(job_id)
    else:
        print(f"No job with id {job_id} found.")
    
    user_email = booking.user.email  
    
    if status == "accepted":
      
        send_email.delay({
            "to_email" : user_email,
            "subject" : "🚑 Booking Accepted - LifeLineGo",
            "body" : "Your ambulance booking request has been accepted. The hospital will assign details soon."
        })

        # Schedule automatic rejection if no details provided in 10 minutes
        scheduler.add_job(
            func=auto_reject_booking,
            trigger="date",
            run_date=datetime.utcnow() + timedelta(minutes=15),
            args=[current_app._get_current_object(), booking_id,"Hospital could not provide booking details in time" ],
            id=f"auto_reject_{booking_id}",
            replace_existing=True,
        )
    
    else:
        send_email.delay({
            "to_email" : user_email,
            "subject" : "❌ Booking Rejected - LifeLineGo",
            "body" : f"Your ambulance booking request has been rejected by the hospital. Please try again.\n Reason : {reason}"
        })


    return {"message": f"Booking request {status} successfully.", "data":booking.to_dict(),"status":200}, 200



def assign_booking_details(data, booking_request_id, hospital_id):
    """Step 2: Hospital assigns driver & ambulance details, generates OTP."""
    booking_request = BookingRequestModel.query.filter_by(id=booking_request_id).first()
    if not booking_request or booking_request.status != "accepted":
        abort(400, message="Booking request is not in an accepted state.")
    
    if str(booking_request.hospital_id) != hospital_id:
        abort(403, message="Access forbidden: Booking request not for this hospital.")
        
    booking = BookingModel.query.filter_by(request_id=booking_request_id).first()
    print("So u called me?")
    if booking:
        abort(400, description={
            "message": "Details have already been provided!",
            "old_booking": booking.to_dict()
        })



    # Generate a 6-digit OTP
    otp_code = random.randint(100000, 999999)

    try:
        # Create Booking Entry
        booking = BookingModel(
            request_id=booking_request.id,
            status="pending",
            ambulance_details=data["ambulance"],
            driver_details=data["driver"],
            otp=OTPModel(  # Creating OTP via the relationship
                otp_code=str(otp_code),  # Storing as string in case of leading zeros
                expires_at=datetime.utcnow() + timedelta(minutes=10)
            )
        )

        db.session.add(booking)
        db.session.commit()  # Commit everything in one transaction
    except IntegrityError as e:
        db.session.rollback()
        print(f"the error was {e}")
        abort(400, message="Invalid data. Could not assign booking details.")
    except Exception as e:
        db.session.rollback()
        print("Exception:", str(e))
        abort(500, message="An error occurred while assigning booking details.")

    

    # Remove auto-reject scheduler
    try:
        scheduler.remove_job(f"auto_reject_{booking_request_id}")
    except Exception:
        current_app.logger.info(f"No auto-reject job found for booking request {booking_request_id}")

    # Get user details
    user_email = booking_request.user.email
    user_phone = booking_request.user.phone  # Assuming phone number is stored

    # Notify user via email
    send_email.delay({
        "to_email" : user_email,
        "subject" : "✅ Booking Confirmed - LifeLineGo",
        "body" : f"Your ambulance and driver have been assigned.\n\n"
        f"🚑 **Ambulance Details**:\n"
        f"• Vehicle Number: {data['ambulance']['vehicle_number']}\n"
        f"• Type: {data['ambulance']['vehicle_type']}\n\n"
        f"👨‍⚕️ **Driver Details**:\n"
        f"• Name: {data['driver']['name']}\n"
        f"• Phone: {data['driver']['phone']}\n\n"
        f"🔑 **Your OTP for booking verification:** {otp_code}\n\n"
        f"Use this OTP to confirm the completion of your booking."
    })

    return {"message": "Booking details assigned successfully. OTP sent via email "}, 200



def get_order_requests(id,role):
    """Retrieve order requests for the logged-in user or hospital."""
    if role not in ["user", "hospital"]:
        abort(403, message="Access forbidden: Only users and hospitals can retrieve order requests.")

    if role == "user":
        order_requests = BookingRequestModel.query.filter_by(user_id=id).all()
    else:  # role == "hospital"
        order_requests = BookingRequestModel.query.filter_by(hospital_id=id).all()



    if not order_requests:
        return {"message": "No order requests found.", "data": []}, 200

    return {
        "message": "Order requests retrieved successfully.",
        "data": [order.to_dict() for order in order_requests],
    }, 200



def auto_reject_booking(app, booking_id, reason):
    """Automatically reject the booking if details aren’t provided in 15 minutes."""
    with app.app_context():
        print("called scheduler")
        booking = BookingRequestModel.query.get(booking_id)
        if booking and booking.status in ["accepted", "pending"]:
            booking.status = "rejected"
            db.session.commit()
            
            # Fetch user email
            user_email = booking.user.email  

            # Send rejection email with reason
            send_email.delay({
                "to_email": user_email,
                "subject": "❌ Booking Auto-Rejected - LifeLineGo",
                "body": f"Your booking has been automatically rejected. Reason: {reason}"
            })
