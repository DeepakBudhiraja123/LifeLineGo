from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from db import db

# Association table for many-to-many relationship between hospitals and drivers
hospital_driver_association = db.Table(
    "hospital_driver",
    db.Column("hospital_id", db.Integer, db.ForeignKey("hospitals.id"), primary_key=True),
    db.Column("driver_id", db.Integer, db.ForeignKey("drivers.id"), primary_key=True)
)

# Address Model
class AddressModel(db.Model):
    __tablename__ = "addresses"

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(200), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    hospitals = db.relationship("HospitalModel", back_populates="address")
    drivers = db.relationship("DriverModel", back_populates="address")


# Admin Model
class AdminModel(db.Model):
    __tablename__ = "admins"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    phone = db.Column(db.String(15), unique=True, nullable=False)

    # Relationship
    hospitals = db.relationship("HospitalModel", back_populates="admin")


# User Model (Patient)
class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship
    bookings = db.relationship("BookingModel", back_populates="user")


# Hospital Model
class HospitalModel(db.Model):
    __tablename__ = "hospitals"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    password = db.Column(db.String(200), nullable=False)
    
    # Foreign keys
    admin_id = db.Column(db.Integer, db.ForeignKey("admins.id"), nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey("addresses.id"), nullable=False)

    # Relationships
    admin = db.relationship("AdminModel", back_populates="hospitals")
    ambulances = db.relationship("AmbulanceModel", back_populates="hospital")
    address = db.relationship("AddressModel", back_populates="hospitals")
    bookings = db.relationship("BookingModel", back_populates="hospital")
    drivers = db.relationship("DriverModel", secondary=hospital_driver_association, back_populates="hospitals")


# Driver Model
class DriverModel(db.Model):
    __tablename__ = "drivers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    status = db.Column(db.String(50), nullable=False, default="available") 
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Foreign key
    address_id = db.Column(db.Integer, db.ForeignKey("addresses.id"), nullable=False)

    # Relationships
    address = db.relationship("AddressModel", back_populates="drivers")
    hospitals = db.relationship("HospitalModel", secondary=hospital_driver_association, back_populates="drivers")
    ambulance = db.relationship("AmbulanceModel", back_populates="driver", uselist=False)  # One-to-one relationship with AmbulanceModel


# Ambulance Model
class AmbulanceModel(db.Model):
    __tablename__ = "ambulances"

    id = db.Column(db.Integer, primary_key=True)
    vehicle_number = db.Column(db.String(20), unique=True, nullable=False)
    vehicle_type = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False, default="available")  # e.g., available, busy, maintenance
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Foreign keys
    hospital_id = db.Column(db.Integer, db.ForeignKey("hospitals.id"), nullable=False)
    driver_id = db.Column(db.Integer, db.ForeignKey("drivers.id"), nullable=True)  # Assigned driver

    # Relationships
    hospital = db.relationship("HospitalModel", back_populates="ambulances")
    driver = db.relationship("DriverModel", back_populates="ambulance", uselist=False)  # One-to-one relationship

# Booking Model
class BookingModel(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(100), nullable=False)
    patient_contact = db.Column(db.String(15), unique=True, nullable=False)
    status = db.Column(db.String(50), nullable=False, default="pending")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    hospital_id = db.Column(db.Integer, db.ForeignKey("hospitals.id"), nullable=False)
    ambulance_id = db.Column(db.Integer, db.ForeignKey("ambulances.id"), nullable=True)
    pickup_address_id = db.Column(db.Integer, db.ForeignKey("addresses.id"), nullable=False)
    destination_address_id = db.Column(db.Integer, db.ForeignKey("addresses.id"), nullable=False)
    driver_id = db.Column(db.Integer, db.ForeignKey("drivers.id"), nullable=True)

    # Relationships
    user = db.relationship("UserModel", back_populates="bookings")
    hospital = db.relationship("HospitalModel", back_populates="bookings")
    ambulance = db.relationship("AmbulanceModel",backref="bookings")
    pickup_address = db.relationship("AddressModel", foreign_keys=[pickup_address_id])
    destination_address = db.relationship("AddressModel", foreign_keys=[destination_address_id])
    driver = db.relationship("DriverModel", backref="bookings")  # New relationship for driver


class TokenBlocklist(db.Model):
    __tablename__ = "token_blocklist"

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
