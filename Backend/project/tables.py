from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from project.db import db

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


class BookingRequestModel(db.Model):
    __tablename__ = "booking_requests"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    hospital_id = db.Column(db.Integer, db.ForeignKey("hospital.id"), nullable=False)
    name = db.Column(db.String(100), nullable=False),
    age = db.Column(db.Integer, nullable=False),
    sex = db.Column(db.Enum("M", "F", "O", name="sex_enum"), nullable=False)
    ambulance_type = db.Column(
        db.Enum("Basic", "Advanced", "ICU", "Neonatal", name="ambulance_type_enum"),
        nullable=False,
        default="Basic"
    )
    status = db.Column(
        db.Enum("pending", "accepted", "rejected", "completed", name="request_status"),
        nullable=False,
        default="pending",
    )

    # New field for rejection reason
    reason_of_rejection = db.Column(db.String(255), nullable=True)

    # Inline address fields
    street = db.Column(db.String(255))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    
    # Foreign key to CityStateModel
    city_state_id = db.Column(db.Integer, db.ForeignKey('city_states.id'), nullable=False)
    city_state = db.relationship('CityStateModel') 

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = db.relationship("UserModel", back_populates="booking_requests")
    hospital = db.relationship("HospitalModel", back_populates="booking_requests")

    def to_dict(self):
        """
        Convert object to dictionary.
        """
        return {
            "id": self.id,
            "pickup_address": {
                "street": self.street,
                "latitude": self.latitude,
                "longitude": self.longitude,
                "city": self.city_state.city if self.city_state else None,
                "state": self.city_state.state if self.city_state else None,
                "postal_code": self.city_state.postal_code if self.city_state else None
            },
            "status": self.status,
            "reason_of_rejection": self.reason_of_rejection,  # Include in dict
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "user_id": self.user_id,
            "hospital_id": self.hospital_id,
            "ambulance_type": self.ambulance_type
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
    booking_requests = db.relationship("BookingRequestModel", back_populates="user")
    
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
    connection_requests = db.relationship("ConnectRequestModel", back_populates="hospital")
    booking_requests = db.relationship("BookingRequestModel", back_populates="hospital") 
    
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
    # bookings = db.relationship("BookingModel", back_populates="driver")
    connection_requests = db.relationship("ConnectRequestModel", back_populates="driver")
    
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


class BookingModel(db.Model):
    __tablename__ = "booking"

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(
        db.Enum("pending", "active", "completed", name="booking_status"), 
        nullable=False, 
        default="pending"
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Reference to Booking Request
    request_id = db.Column(db.Integer, db.ForeignKey("booking_requests.id"), nullable=False, unique=True)
    request = db.relationship("BookingRequestModel")
    # Relationship with Booking
    otp = db.relationship("OTPModel",  uselist=False)

    # Store Driver & Ambulance details as JSON instead of foreign keys
    ambulance_details = db.Column(db.JSON, nullable=False)
    driver_details = db.Column(db.JSON, nullable=False)

    def to_dict(self):
        return {
            "bookingId": self.id,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "request_id": self.request_id,
            "ambulance_details": self.ambulance_details,
            "driver_details": self.driver_details
        }



class TokenBlocklist(db.Model):
    __tablename__ = "token_blocklist"

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)


class ConnectRequestModel(db.Model):
    __tablename__ = "connect_requests"
    
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Enum("pending", "accepted", "rejected", name="request_status"), nullable=False, default="pending")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Request sender type: 'driver' or 'hospital'
    sender_type = db.Column(db.Enum("driver", "hospital", name="sender_type"), nullable=False)

    # Foreign keys
    driver_id = db.Column(db.Integer, db.ForeignKey('driver.id'), nullable=False)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospital.id'), nullable=False)
    
    # Relationships with back_populates
    driver = db.relationship("DriverModel", back_populates="connection_requests")
    hospital = db.relationship("HospitalModel", back_populates="connection_requests")

    def to_dict(self):
        return {
            "id": self.id,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "sender_type": self.sender_type,
            "driver": self.driver.to_dict(),
            "hospital": self.hospital.to_dict()
        }


class OTPModel(db.Model):
    __tablename__ = "otp"

    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey("booking.id"), nullable=False, unique=True)
    otp_code = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "booking_id": self.booking_id,
            "otp_code": self.otp_code,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None
        }
