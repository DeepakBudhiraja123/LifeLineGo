from datetime import datetime
from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import IntegrityError
from flask_smorest import abort
from db import db
from tables import AddressModel, DriverModel, BookingModel
from tables import hospital_driver_association
from schemas import DriverSchema
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

def create_driver_logic(data):
    """Create a new driver along with an address."""
    # Create and save the address first
    address = AddressModel(
        address=data["address"],
        latitude=data["latitude"],
        longitude=data["longitude"]
    )
    db.session.add(address)
    db.session.flush()  # Ensure we get the address ID before committing

    # Create the driver with hashed password and address_id
    driver = DriverModel(
        name=data["name"],
        email=data["email"],
        phone=data["phone"],
        password=pbkdf2_sha256.hash(data["password"]),  # Hashing password using passlib
        address_id=address.id,
        status=data.get("status", "available"),
        created_at=datetime.utcnow()
    )
    db.session.add(driver)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        abort(400, message="Driver with this email or phone or name already exists.")
    
    access_token = create_access_token(identity=str(driver.id), additional_claims={"role": "driver"}, fresh=True)
    refresh_token = create_refresh_token(identity=str(driver.id),additional_claims={"role": "driver"},)
    return {
        "driver":DriverSchema().dump(driver),
        "access_token": access_token,
        "refresh_token": refresh_token
    }



def delete_driver_logic(driver_id):
    """Delete a driver after checking active bookings."""
    driver = get_driver_logic(driver_id)
    if is_driver_in_active_booking(driver.id):
        abort(400, message="Cannot delete driver with active bookings.")
    
    db.session.delete(driver)
    db.session.commit()



def login_driver_logic(driver_data):
    """Business logic to log in a user."""
    driver = DriverModel.query.filter_by(name=driver_data["name"]).first()
    if not driver or not pbkdf2_sha256.verify(driver_data["password"], driver.password):
        abort(401, message="Invalid username or password.")
    
    access_token = create_access_token(identity=str(driver.id), additional_claims={"role": "driver"}, fresh=True)
    refresh_token = create_refresh_token(identity=str(driver.id),additional_claims={"role": "driver"})
    
    return {
        "message": "Login successful",
        "access_token": access_token,
        "refresh_token": refresh_token
    }


def get_driver_logic(driver_id):
    """Business logic to get a user by ID."""
    driver = DriverModel.query.get(driver_id)
    if not driver:
        abort(404, message="Drivernot found.")
    return driver



def get_all_drivers_logic():
    """Fetch all drivers from the database."""
    drivers = DriverModel.query.all()
    driver_schema =DriverSchema(many=True)  # Serialize a list of drivers
    return driver_schema.dump(drivers)


def update_driver_logic(driver_id, driver_data):
    try:
        driver = DriverModel.query.get(driver_id)
        if not driver:
            return {"message": "Driver not found"}, 404
        if 'password' in driver_data:
            if len(driver_data["password"]) < 6:
                abort(400, message="Password must be at least 6 characters long.")
            driver_data["password"] = pbkdf2_sha256.hash(driver_data["password"])
        # Update fields
        driver.name = driver_data.get("name", driver.name)
        driver.email = driver_data.get("email", driver.email)
        driver.phone = driver_data.get("phone", driver.phone)
        driver.address.address = driver_data.get("location", driver.address.address)
        driver.address.latitude = driver_data.get("latitude", driver.address.latitude)
        driver.address.longitude = driver_data.get("longitude", driver.address.longitude)
        driver.password = driver_data.get("password", driver.password)
        
        db.session.commit()
        return driver

    except IntegrityError as e:
        db.session.rollback()
        if "email" in str(e.orig):
            return {"message": "A driver with this email already exists"}, 400
        elif "name" in str(e.orig):
            return {"message": "A driver with this name already exists"}, 400
        elif "phone" in str(e.orig):
            return {"message": "A driver with this phone number already exists"}, 400
        else:
            return {"message": "An unexpected error occurred"}, 500

