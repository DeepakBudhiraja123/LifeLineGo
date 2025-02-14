from datetime import datetime
from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import IntegrityError
from flask_smorest import abort
from db import db
from tables import *
from schemas import DriverSchema, PlainAddressSchema
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token
)



def driver_exists(driver_id):
    """Check if the driver exists in the database."""
    return DriverModel.query.get(driver_id) is not None

def is_driver_associated_with_hospital(driver_id, hospital_id):
    """Check if the driver is associated with the given hospital."""
    return hospital_driver_association.query.filter_by(driver_id=driver_id, hospital_id=hospital_id).first() is not None

def is_driver_in_active_booking(driver_id):
    """Check if the driver is involved in any active booking."""
    return BookingModel.query.filter_by(driver_id=driver_id, status="active").first() is not None

def connect_driver_with_hospital(driver_id, hospital_ids):
    """Connect the driver with the hospital."""
    driver = DriverModel.query.get(driver_id)
    hospitals = [HospitalModel.query.get(hospital_id) for hospital_id in hospital_ids]
    driver.hospitals.extend(hospitals)
    


        
        
    

