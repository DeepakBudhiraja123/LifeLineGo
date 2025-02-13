from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from db import db

# Association table for many-to-many relationship between hospitals and drivers
hospital_driver_association = db.Table(
    "hospital_driver",
    db.Column("hospital_id", db.Integer, db.ForeignKey("hospital.id"), primary_key=True),
    db.Column("driver_id", db.Integer, db.ForeignKey("driver.id"), primary_key=True)
)

class CityStateModel(db.Model):
    __tablename__ = "city_states"
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    postal_code = db.Column(db.String(20), nullable=False, unique=True)
 
    
    def to_dict(self):
        return {
            "id": self.id,
            "city": self.city,
            "state": self.state,
            "postal_code": self.postal_code
        }


# Admin Model
class AdminModel(db.Model):
    __tablename__ = "admin"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "phone": self.phone
        }



# User Model (Patient)
class UserModel(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    bookings = db.relationship("BookingModel", back_populates="user")
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }



# Hospital Model
class HospitalModel(db.Model):
    __tablename__ = "hospital"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    password = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    
    # Inline address fields
    street = db.Column(db.String(255))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    
    # Foreign key to CityStateModel
    city_state_id = db.Column(db.Integer, db.ForeignKey('city_states.id'), nullable=False)
    city_state = db.relationship('CityStateModel')

    # Relationships
    ambulances = db.relationship("AmbulanceModel", backref="hospital")
    drivers = db.relationship("DriverModel", secondary=hospital_driver_association, back_populates="hospitals")
    bookings = db.relationship("BookingModel", back_populates="hospital")
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "phone": self.phone,
            "address": {
                "street": self.street,
                "latitude": self.latitude,
                "longitude": self.longitude,
                "city": self.city_state.city if self.city_state else None,
                "state": self.city_state.state if self.city_state else None,
                "postal_code": self.city_state.postal_code if self.city_state else None
            }
        }



# Driver Model
class DriverModel(db.Model):
    __tablename__ = "driver"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Enum("available", "busy", "off-duty", name="driver_status"), nullable=False, default="available")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Inline address fields
    street = db.Column(db.String(255))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    
    # Foreign key to CityStateModel
    city_state_id = db.Column(db.Integer, db.ForeignKey('city_states.id'), nullable=False)
    city_state = db.relationship('CityStateModel')
    
    # Relationships
    hospitals = db.relationship("HospitalModel", secondary=hospital_driver_association, back_populates="drivers")
    bookings = db.relationship("BookingModel", back_populates="driver")
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "address": {
                "street": self.street,
                "latitude": self.latitude,
                "longitude": self.longitude,
                "city": self.city_state.city if self.city_state else None,
                "state": self.city_state.state if self.city_state else None,
                "postal_code": self.city_state.postal_code if self.city_state else None
            }
        }



# Ambulance Model
class AmbulanceModel(db.Model):
    __tablename__ = "ambulance"

    id = db.Column(db.Integer, primary_key=True)
    vehicle_number = db.Column(db.String(20), unique=True, nullable=False)
    vehicle_type = db.Column(db.String(50), nullable=False)
    status = db.Column(db.Enum("available", "busy", "maintenance", name="ambulance_status"), nullable=False, default="available")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Foreign keys
    hospital_id = db.Column(db.Integer, db.ForeignKey("hospital.id"), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "vehicle_number": self.vehicle_number,
            "vehicle_type": self.vehicle_type,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "hospital": self.hospital.to_dict()
        }


# Booking Model
class BookingModel(db.Model):
    __tablename__ = "booking"

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50), nullable=False, default="pending")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Inline address fields
    source_street = db.Column(db.String(255))
    source_latitude = db.Column(db.Float)
    source_longitude = db.Column(db.Float)
    
    # Foreign key to CityStateModel
    source_city_state_id = db.Column(db.Integer, db.ForeignKey('city_states.id'), nullable=False)
    source_city_state = db.relationship('CityStateModel')

    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    hospital_id = db.Column(db.Integer, db.ForeignKey("hospital.id"), nullable=False)
    ambulance_id = db.Column(db.Integer, db.ForeignKey("ambulance.id"), nullable=True)
    driver_id = db.Column(db.Integer, db.ForeignKey("driver.id"), nullable=True)

    # Relationships
    user = db.relationship("UserModel", back_populates="bookings")
    hospital = db.relationship("HospitalModel", back_populates="bookings")
    ambulance = db.relationship("AmbulanceModel")
    driver = db.relationship("DriverModel", back_populates="bookings", foreign_keys=[driver_id])  # New relationship for driver
    
    def to_dict(self):
        return {
            "bookingId": self.id,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "pickup_address": {
                "street": self.source_street,
                "latitude": self.source_latitude,
                "longitude": self.source_longitude,
                "city": self.source_city_state.city if self.source_city_state else None,
                "state": self.source_city_state.state if self.source_city_state else None,
                "postal_code": self.source_city_state.postal_code if self.source_city_state else None
            },
            "user": self.user.to_dict(),
            "hospital": self.hospital.to_dict(),
            "ambulance": self.ambulance.to_dict() if self.ambulance else None,
            "driver": self.driver.to_dict() if self.driver else None
        }


class TokenBlocklist(db.Model):
    __tablename__ = "token_blocklist"

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)



