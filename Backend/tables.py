from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from db import db

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
    phone = db.Column(db.String(15), unique=True,nullable=False)

    # Relationship
    hospitals = db.relationship("HospitalModel", back_populates="admin")


# User Model (Patient)
class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(15),unique=True, nullable=False)
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


# Driver Model
class DriverModel(db.Model):
    __tablename__ = "drivers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(15),unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Foreign key
    address_id = db.Column(db.Integer, db.ForeignKey("addresses.id"), nullable=False)

    # Relationship
    address = db.relationship("AddressModel", back_populates="drivers")


# Ambulance Model
class AmbulanceModel(db.Model):
    __tablename__ = "ambulances"

    id = db.Column(db.Integer, primary_key=True)
    vehicle_number = db.Column(db.String(20), unique=True, nullable=False)
    vehicle_type = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Foreign key
    hospital_id = db.Column(db.Integer, db.ForeignKey("hospitals.id"), nullable=False)

    # Relationship
    hospital = db.relationship("HospitalModel", back_populates="ambulances")


# Booking Model
class BookingModel(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)
    patient_name = db.Column(db.String(100), nullable=False)
    patient_contact = db.Column(db.String(15),unique=True, nullable=False)
    status = db.Column(db.String(50), nullable=False, default="pending")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    hospital_id = db.Column(db.Integer, db.ForeignKey("hospitals.id"), nullable=False)
    ambulance_id = db.Column(db.Integer, db.ForeignKey("ambulances.id"), nullable=True)
    pickup_address_id = db.Column(db.Integer, db.ForeignKey("addresses.id"), nullable=False)
    destination_address_id = db.Column(db.Integer, db.ForeignKey("addresses.id"), nullable=False)

    # Relationships
    user = db.relationship("UserModel", back_populates="bookings")
    hospital = db.relationship("HospitalModel",back_populates="bookings")
    ambulance = db.relationship("AmbulanceModel")
    pickup_address = db.relationship("AddressModel", foreign_keys=[pickup_address_id])
    destination_address = db.relationship("AddressModel", foreign_keys=[destination_address_id])

