from marshmallow import Schema, fields
from enum import Enum

# ===================== User Schemas ===================== #
class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(load_only=True, required=True)
    phone = fields.Str(required=True)

class AddressSchema(Schema):
    id = fields.Int(dump_only=True)
    street = fields.Str(required=True)
    city = fields.Str(required=True)
    state = fields.Str(required=True)
    postal_code = fields.Str(required=True)
    latitude = fields.Float(required=True)
    longitude = fields.Float(required=True)
    


class AmbulanceTypeEnum(Enum):
    BASIC = "Basic"
    ADVANCED = "Advanced"
    ICU = "ICU"
    NEONATAL = "Neonatal"
    
# Define Enum
class SexEnum(Enum):
    MALE = "M"
    FEMALE = "F"
    OTHER = "O"

class OrderRequestSchema(Schema):
    hospital_id = fields.Int(required=True)  # ForeignKey to Hospital
    ambulance_type = fields.Str(required=True, validate=lambda x: x in AmbulanceTypeEnum._value2member_map_)
    address = fields.Nested(AddressSchema, required=True)  # Nested Address object
    status = fields.Str(
        required=True, 
        validate=lambda x: x in ["pending", "accepted", "rejected", "completed"],
        default="Pending"
    )
     # User details
    name = fields.Str(required=True)
    age = fields.Int(required=True)
    sex = fields.Str(required=True, validate=lambda x: x in SexEnum._value2member_map_)


class PlainHospitalSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    phone = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(load_only=True, required=True)
    created_at = fields.DateTime(dump_only=True)

class DriverSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    phone = fields.Str(required=True)

class AmbulanceSchema(Schema):
    vehicle_number = fields.Str(required=True)
    vehicle_type = fields.Str(required=True)  # "basic", "advanced"


class HospitalSchema(PlainHospitalSchema):
    address = fields.Nested(AddressSchema, required=True)



class BookingSchema(Schema):
    driver = fields.Nested(DriverSchema, required=True)
    ambulance = fields.Nested(AmbulanceSchema, required=True)



class AdminSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(load_only=True, required=True)
    phone = fields.Str(required=True)


class LoginSchema(Schema):
    name = fields.Str(required=True)
    password = fields.Str(required=True)
